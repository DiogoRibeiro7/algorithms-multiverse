"""
PDF Report Generator - Creates professional PDF reports
"""

from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("ReportLab not available - PDF generation will be disabled")


class PDFReportGenerator:
    """Generates professional PDF performance reports"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def generate(self, results: Dict[str, Any], output_dir: Path) -> Path:
        """
        Generate PDF report

        Args:
            results: Analysis results
            output_dir: Output directory

        Returns:
            Path to generated PDF file
        """
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not installed - cannot generate PDF")
            # Create a placeholder file
            output_path = output_dir / 'report.pdf'
            output_path.write_text("PDF generation requires reportlab package")
            return output_path

        output_path = output_dir / 'report.pdf'

        # Create PDF document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        # Build document content
        story = []
        styles = getSampleStyleSheet()

        # Add custom styles
        self._add_custom_styles(styles)

        # Build sections
        story.extend(self._title_page(results, styles))
        story.append(PageBreak())

        story.extend(self._executive_summary(results, styles))
        story.append(PageBreak())

        story.extend(self._performance_overview(results, styles))
        story.append(PageBreak())

        story.extend(self._detailed_results(results, styles))
        story.append(PageBreak())

        story.extend(self._recommendations(results, styles))

        # Build PDF
        doc.build(story)

        logger.info(f"Generated PDF report: {output_path}")
        return output_path

    def _add_custom_styles(self, styles):
        """Add custom paragraph styles"""
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Section heading
        styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12
        ))

        # Subsection heading
        styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6
        ))

    def _title_page(self, results: Dict[str, Any], styles) -> List:
        """Generate title page"""
        story = []

        # Title
        title = Paragraph("Performance Analysis Report", styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 0.5 * inch))

        # Metadata
        timestamp = datetime.fromisoformat(results['timestamp'])
        date_str = timestamp.strftime('%B %d, %Y at %H:%M:%S')

        metadata = [
            ['Run ID:', results['run_id']],
            ['Date:', date_str],
            ['Categories:', ', '.join(results['benchmarks'].keys())],
            ['Total Benchmarks:', str(results['statistics']['summary']['total_benchmarks'])],
            ['Languages Tested:', str(results['statistics']['summary']['total_languages'])]
        ]

        table = Table(metadata, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONT', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#7f8c8d')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(table)

        return story

    def _executive_summary(self, results: Dict[str, Any], styles) -> List:
        """Generate executive summary section"""
        story = []

        story.append(Paragraph("Executive Summary", styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))

        stats = results['statistics']['summary']

        # Summary text
        summary_text = f"""
        This report presents a comprehensive performance analysis of {stats['total_benchmarks']}
        algorithm implementations across {stats['total_languages']} programming languages.
        """

        story.append(Paragraph(summary_text, styles['BodyText']))
        story.append(Spacer(1, 0.2 * inch))

        # Key findings
        story.append(Paragraph("Key Findings", styles['SubsectionHeading']))

        findings = []

        # Fastest overall
        if stats['fastest_overall'] and stats['fastest_overall']['time'] != float('inf'):
            fastest = stats['fastest_overall']
            findings.append(
                f"<b>Fastest Implementation:</b> {fastest['algorithm']} ({fastest['language']}) "
                f"with {fastest['time']:.2f}ms average execution time"
            )

        # Regressions
        if 'trends' in results:
            regression_count = results['trends']['summary']['total_regressions']
            improvement_count = results['trends']['summary']['total_improvements']

            if regression_count > 0:
                findings.append(
                    f"<b>⚠ Performance Regressions:</b> {regression_count} algorithms "
                    f"showing performance degradation"
                )

            if improvement_count > 0:
                findings.append(
                    f"<b>✓ Performance Improvements:</b> {improvement_count} algorithms "
                    f"showing performance gains"
                )

        if not findings:
            findings.append("All benchmarks completed successfully with stable performance")

        for finding in findings:
            story.append(Paragraph(f"• {finding}", styles['BodyText']))
            story.append(Spacer(1, 0.1 * inch))

        return story

    def _performance_overview(self, results: Dict[str, Any], styles) -> List:
        """Generate performance overview section"""
        story = []

        story.append(Paragraph("Performance Overview", styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))

        # Top performers table
        story.append(Paragraph("Top Performers", styles['SubsectionHeading']))

        if 'comparisons' in results['statistics']:
            comparisons = results['statistics']['comparisons']

            # Sort by performance
            sorted_comparisons = sorted(
                comparisons.items(),
                key=lambda x: x[1]['fastest']['avg_time_ms']
            )[:10]

            table_data = [['Rank', 'Algorithm', 'Language', 'Avg Time', 'Category']]

            for rank, (key, data) in enumerate(sorted_comparisons, 1):
                parts = key.split('/')
                category = parts[0] if parts else 'N/A'
                algorithm = parts[1] if len(parts) > 1 else 'N/A'

                fastest = data['fastest']
                table_data.append([
                    str(rank),
                    algorithm,
                    fastest['language'],
                    f"{fastest['avg_time_ms']:.2f}ms",
                    category
                ])

            table = Table(table_data, colWidths=[0.5 * inch, 1.5 * inch, 1 * inch, 1 * inch, 1.5 * inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))

            story.append(table)

        story.append(Spacer(1, 0.3 * inch))

        # Language rankings
        if 'recommendations' in results and 'language_selection' in results['recommendations']:
            lang_rec = results['recommendations']['language_selection']

            story.append(Paragraph("Language Performance Rankings", styles['SubsectionHeading']))

            if 'rankings' in lang_rec:
                table_data = [['Rank', 'Language', 'Avg Time', 'Benchmarks', 'Win Rate']]

                for rank, lang_data in enumerate(lang_rec['rankings'][:10], 1):
                    table_data.append([
                        str(rank),
                        lang_data['language'],
                        f"{lang_data['avg_time_ms']:.2f}ms",
                        str(lang_data['benchmarks']),
                        f"{lang_data['win_rate']:.0f}%"
                    ])

                table = Table(table_data, colWidths=[0.5 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]))

                story.append(table)

        return story

    def _detailed_results(self, results: Dict[str, Any], styles) -> List:
        """Generate detailed results section"""
        story = []

        story.append(Paragraph("Detailed Benchmark Results", styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))

        for category, algorithms in results['benchmarks'].items():
            story.append(Paragraph(
                category.replace('-', ' ').title(),
                styles['SubsectionHeading']
            ))

            for algorithm, languages in algorithms.items():
                # Algorithm name
                story.append(Paragraph(f"<b>{algorithm}</b>", styles['BodyText']))
                story.append(Spacer(1, 0.1 * inch))

                # Results table
                table_data = [['Language', 'Avg Time', 'Median', 'Std Dev', 'Min', 'Max']]

                for language, data in languages.items():
                    if 'error' in data:
                        table_data.append([language, 'Error', '-', '-', '-', '-'])
                    else:
                        table_data.append([
                            language,
                            f"{data['avg_time_ms']:.2f}ms",
                            f"{data['median_time_ms']:.2f}ms",
                            f"{data['stdev_time_ms']:.2f}ms",
                            f"{data['min_time_ms']:.2f}ms",
                            f"{data['max_time_ms']:.2f}ms"
                        ])

                table = Table(table_data, colWidths=[1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ecf0f1')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ]))

                story.append(table)
                story.append(Spacer(1, 0.2 * inch))

        return story

    def _recommendations(self, results: Dict[str, Any], styles) -> List:
        """Generate recommendations section"""
        story = []

        story.append(Paragraph("Recommendations", styles['SectionHeading']))
        story.append(Spacer(1, 0.2 * inch))

        if 'recommendations' not in results:
            story.append(Paragraph("No recommendations available", styles['BodyText']))
            return story

        recommendations = results['recommendations']

        # Algorithm recommendations
        if 'algorithm_selection' in recommendations and recommendations['algorithm_selection']:
            story.append(Paragraph("Algorithm Selection", styles['SubsectionHeading']))

            for rec in recommendations['algorithm_selection'][:5]:
                rec_text = f"""
                <b>{rec['category']}:</b><br/>
                • Recommended: <b>{rec['recommended']}</b> - {rec['reason']}<br/>
                """

                if rec.get('avoid'):
                    rec_text += f"• Avoid: <b>{rec['avoid']}</b> - {rec['avoid_reason']}<br/>"

                story.append(Paragraph(rec_text, styles['BodyText']))
                story.append(Spacer(1, 0.15 * inch))

        # Language recommendations
        if 'language_selection' in recommendations:
            lang_rec = recommendations['language_selection']

            story.append(Paragraph("Language Selection", styles['SubsectionHeading']))

            if 'recommendation' in lang_rec:
                story.append(Paragraph(lang_rec['recommendation'], styles['BodyText']))
                story.append(Spacer(1, 0.15 * inch))

        # Best practices
        if 'best_practices' in recommendations and recommendations['best_practices']:
            story.append(Paragraph("Best Practices", styles['SubsectionHeading']))

            for practice in recommendations['best_practices'][:5]:
                practice_text = f"<b>{practice['category']}:</b> {practice['practice']}"
                story.append(Paragraph(f"• {practice_text}", styles['BodyText']))
                story.append(Spacer(1, 0.1 * inch))

        return story
