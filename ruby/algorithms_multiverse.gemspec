# frozen_string_literal: true

Gem::Specification.new do |spec|
  spec.name = "algorithms_multiverse"
  spec.version = "1.0.0"
  spec.authors = ["Algorithms Multiverse"]
  spec.email = ["contact@algorithms-multiverse.com"]

  spec.summary = "Comprehensive algorithm implementations in Ruby"
  spec.description = "A collection of fundamental algorithms and data structures implemented in idiomatic Ruby with performance optimizations"
  spec.homepage = "https://github.com/algorithms-multiverse/ruby"
  spec.license = "MIT"
  spec.required_ruby_version = ">= 2.7.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/algorithms-multiverse/ruby"
  spec.metadata["documentation_uri"] = "https://rubydoc.info/gems/algorithms_multiverse"
  spec.metadata["changelog_uri"] = "https://github.com/algorithms-multiverse/ruby/blob/main/CHANGELOG.md"

  spec.files = Dir.chdir(File.expand_path(__dir__)) do
    Dir["{lib}/**/*", "LICENSE", "README.md", "CHANGELOG.md"]
  end
  spec.require_paths = ["lib"]

  # Development dependencies
  spec.add_development_dependency "bundler", "~> 4.0"
  spec.add_development_dependency "rake", "~> 13.0"
  spec.add_development_dependency "rspec", "~> 3.0"
  spec.add_development_dependency "rubocop", "~> 1.0"
  spec.add_development_dependency "rubocop-performance", "~> 1.0"
  spec.add_development_dependency "rubocop-rspec", "~> 2.0"
  spec.add_development_dependency "simplecov", "~> 0.21"
  spec.add_development_dependency "yard", "~> 0.9"

  # Runtime dependencies (keeping it minimal)
  spec.add_dependency "concurrent-ruby", "~> 1.0"  # For parallel processing
end