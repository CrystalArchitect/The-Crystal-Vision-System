# Contributing to AUS-Monorepo

Thank you for helping build sovereign, decentralized infrastructure. This guide outlines how to contribute.

## Core Principles

All contributions should reflect these principles:

- **Decentralized**: Design for systems without single points of control
- **Sovereign**: Enable self-governance and trustless coordination
- **Trustless**: Use cryptographic verification, not trust assumptions
- **Open**: Public specifications and transparent processes
- **Resilient**: Build for Byzantine-failure environments
- **Interoperable**: Design clear protocols and standards

## Contribution Types

### Code & Implementation
- Reference implementations of protocols
- Infrastructure components (networking, storage, computation)
- Agent frameworks and coordination systems
- Cryptographic primitives and proofs

### Specifications & Design
- Protocol specifications with formal definitions
- Threat models and security analysis
- Performance analysis and benchmarks
- Integration guides and examples

### Documentation & Research
- Technical documentation and API guides
- Research papers and analysis
- Case studies and real-world applications
- Educational materials

## Getting Started

1. **Read the repo's CLAUDE.md** — understand project conventions
2. **Pick an area** — protocols, agents, governance, cryptography, infrastructure
3. **Start small** — open an issue first for significant changes
4. **Test thoroughly** — include test vectors and verification examples
5. **Document clearly** — assume readers are unfamiliar with your area

## Submission Process

1. Create a branch from `main` (e.g., `feature/your-feature-name`)
2. Make your changes following the repo's structure and conventions
3. Include tests and documentation
4. Open a pull request with a clear description of changes
5. Respond to review comments — we're collaborative

## PR Expectations

- **Specification clarity**: Does this enable other implementations?
- **Test coverage**: Are test vectors or examples included?
- **Security rigor**: Have threat models been considered?
- **Interoperability**: Does this follow established standards?
- **Documentation**: Can others understand and build on this?

## Code Style & Conventions

Follow the conventions established in each language/framework subdirectory. When in doubt:

- Use clear, descriptive names
- Document non-obvious design decisions
- Include examples and usage
- Write for future readers, not just yourself

## Design Review

Significant changes (new protocols, consensus algorithms, cryptographic schemes) benefit from early feedback. Before implementing:

1. Open an issue describing the problem and proposed approach
2. Link to relevant research or prior work
3. Discuss trade-offs and design decisions
4. Iterate with the community before building

## Security Considerations

- Never commit secrets, private keys, or credentials
- Include threat models for cryptographic components
- Document assumptions (e.g., network synchrony, adversary strength)
- Use established standards when available
- Get independent review for security-critical code

## License

All contributions must comply with the repository's license (typically MIT or CC0). By contributing, you agree to license your work under the same terms.

## Questions?

Open an issue, join the community discussions, or reach out to the repository's maintainers. We're here to help.

---

Thank you for contributing to decentralized, sovereign infrastructure! 🚀
