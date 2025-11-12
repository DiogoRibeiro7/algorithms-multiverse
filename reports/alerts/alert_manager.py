"""
Alert Manager - Sends alerts for performance regressions and issues
"""

import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Optional
import urllib.request
import urllib.error

logger = logging.getLogger(__name__)


class AlertManager:
    """Manages alerts for performance issues"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.alert_email = config.get('alert_email')
        self.alert_slack_webhook = config.get('alert_slack_webhook')
        self.smtp_config = config.get('smtp_config', {})

    def send_regression_alert(self, regressions: List[Dict[str, Any]], run_id: str):
        """
        Send alerts for performance regressions

        Args:
            regressions: List of detected regressions
            run_id: Run ID for the analysis
        """
        if not regressions:
            return

        logger.info(f"Sending alerts for {len(regressions)} regression(s)")

        # Prepare alert message
        message = self._format_regression_message(regressions, run_id)

        # Send via configured channels
        if self.alert_email:
            self._send_email_alert(
                subject=f"⚠️ Performance Regression Alert - {run_id}",
                message=message
            )

        if self.alert_slack_webhook:
            self._send_slack_alert(
                title="⚠️ Performance Regression Alert",
                message=message,
                run_id=run_id
            )

    def send_failure_alert(self, failures: List[Dict[str, Any]], run_id: str):
        """
        Send alerts for benchmark failures

        Args:
            failures: List of failed benchmarks
            run_id: Run ID for the analysis
        """
        if not failures:
            return

        logger.info(f"Sending alerts for {len(failures)} failure(s)")

        message = self._format_failure_message(failures, run_id)

        if self.alert_email:
            self._send_email_alert(
                subject=f"❌ Benchmark Failure Alert - {run_id}",
                message=message
            )

        if self.alert_slack_webhook:
            self._send_slack_alert(
                title="❌ Benchmark Failure Alert",
                message=message,
                run_id=run_id
            )

    def send_improvement_alert(self, improvements: List[Dict[str, Any]], run_id: str):
        """
        Send alerts for significant improvements

        Args:
            improvements: List of detected improvements
            run_id: Run ID for the analysis
        """
        if not improvements:
            return

        # Only send if there are significant improvements (>20%)
        significant = [imp for imp in improvements if imp.get('improvement_percent', 0) > 20]

        if not significant:
            return

        logger.info(f"Sending alerts for {len(significant)} significant improvement(s)")

        message = self._format_improvement_message(significant, run_id)

        if self.alert_email:
            self._send_email_alert(
                subject=f"🚀 Performance Improvement Alert - {run_id}",
                message=message
            )

        if self.alert_slack_webhook:
            self._send_slack_alert(
                title="🚀 Performance Improvement Alert",
                message=message,
                run_id=run_id,
                color="good"
            )

    def _format_regression_message(self, regressions: List[Dict[str, Any]], run_id: str) -> str:
        """Format regression alert message"""
        lines = [
            "Performance Regression Detected",
            "=" * 50,
            f"\nRun ID: {run_id}",
            f"Regressions Found: {len(regressions)}\n"
        ]

        for reg in regressions:
            lines.append(
                f"\n🔴 {reg['algorithm']} ({reg['language']})\n"
                f"   Regression: {reg['percent_change']:.1f}% slower\n"
                f"   Baseline: {reg['baseline']:.2f}ms\n"
                f"   Current: {reg['current']:.2f}ms"
            )

        lines.append("\n" + "=" * 50)
        lines.append("Please investigate these performance degradations.")

        return '\n'.join(lines)

    def _format_failure_message(self, failures: List[Dict[str, Any]], run_id: str) -> str:
        """Format failure alert message"""
        lines = [
            "Benchmark Failures Detected",
            "=" * 50,
            f"\nRun ID: {run_id}",
            f"Failures: {len(failures)}\n"
        ]

        for failure in failures:
            lines.append(
                f"\n❌ {failure['algorithm']} ({failure['language']})\n"
                f"   Error: {failure.get('error', 'Unknown error')}"
            )

        lines.append("\n" + "=" * 50)
        lines.append("Please check the logs for more details.")

        return '\n'.join(lines)

    def _format_improvement_message(self, improvements: List[Dict[str, Any]], run_id: str) -> str:
        """Format improvement alert message"""
        lines = [
            "Significant Performance Improvements Detected",
            "=" * 50,
            f"\nRun ID: {run_id}",
            f"Improvements: {len(improvements)}\n"
        ]

        for imp in improvements:
            lines.append(
                f"\n🟢 {imp['algorithm']} ({imp['language']})\n"
                f"   Improvement: {imp['improvement_percent']:.1f}% faster\n"
                f"   Baseline: {imp['baseline']:.2f}ms\n"
                f"   Current: {imp['current']:.2f}ms"
            )

        lines.append("\n" + "=" * 50)
        lines.append("Great work on the optimization!")

        return '\n'.join(lines)

    def _send_email_alert(self, subject: str, message: str):
        """
        Send email alert

        Args:
            subject: Email subject
            message: Email body
        """
        try:
            # Get SMTP configuration
            smtp_host = self.smtp_config.get('host', 'localhost')
            smtp_port = self.smtp_config.get('port', 587)
            smtp_user = self.smtp_config.get('user')
            smtp_password = self.smtp_config.get('password')
            from_email = self.smtp_config.get('from_email', 'noreply@performance.local')

            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = self.alert_email
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            # Send email
            if smtp_user and smtp_password:
                server = smtplib.SMTP(smtp_host, smtp_port)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                server.quit()
                logger.info(f"Email alert sent to {self.alert_email}")
            else:
                logger.warning("SMTP credentials not configured - email not sent")

        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")

    def _send_slack_alert(
        self,
        title: str,
        message: str,
        run_id: str,
        color: str = "danger"
    ):
        """
        Send Slack webhook alert

        Args:
            title: Alert title
            message: Alert message
            run_id: Run ID
            color: Message color (good, warning, danger)
        """
        try:
            # Format Slack message
            slack_message = {
                "attachments": [
                    {
                        "color": color,
                        "title": title,
                        "text": message,
                        "fields": [
                            {
                                "title": "Run ID",
                                "value": run_id,
                                "short": True
                            }
                        ],
                        "footer": "Performance Analysis System",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }

            # Send request
            data = json.dumps(slack_message).encode('utf-8')
            req = urllib.request.Request(
                self.alert_slack_webhook,
                data=data,
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    logger.info("Slack alert sent successfully")
                else:
                    logger.warning(f"Slack alert response: {response.status}")

        except urllib.error.URLError as e:
            logger.error(f"Failed to send Slack alert: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending Slack alert: {e}")

    def send_custom_alert(
        self,
        title: str,
        message: str,
        severity: str = "info",
        run_id: Optional[str] = None
    ):
        """
        Send custom alert

        Args:
            title: Alert title
            message: Alert message
            severity: Severity level (info, warning, error)
            run_id: Optional run ID
        """
        subject_prefix = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌'
        }.get(severity, 'ℹ️')

        color_map = {
            'info': 'good',
            'warning': 'warning',
            'error': 'danger'
        }

        full_message = f"{title}\n\n{message}"
        if run_id:
            full_message += f"\n\nRun ID: {run_id}"

        if self.alert_email:
            self._send_email_alert(
                subject=f"{subject_prefix} {title}",
                message=full_message
            )

        if self.alert_slack_webhook:
            self._send_slack_alert(
                title=f"{subject_prefix} {title}",
                message=message,
                run_id=run_id or "N/A",
                color=color_map.get(severity, 'good')
            )


# Import datetime for timestamps
from datetime import datetime
