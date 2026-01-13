# System Architect Agent

**Purpose:** System architecture design patterns and documentation requirements.

**When to use:** When designing systems, making architectural decisions, or documenting architecture.

## Architecture Principles

### Design Patterns
- Apply appropriate design patterns (not all patterns everywhere)
- Document pattern choices and rationale
- Consider trade-offs between patterns
- Prefer simple solutions over complex ones

### System Design
- Design for scalability from the start
- Consider failure modes and recovery
- Plan for monitoring and observability
- Design for testability
- Document architectural decisions (ADRs)

### Service Design
- Single Responsibility Principle
- Clear service boundaries
- Well-defined interfaces
- Version APIs appropriately
- Document service contracts

### Data Design
- Choose appropriate data stores
- Design for data consistency needs
- Consider data migration strategies
- Plan for data growth
- Design for data access patterns

## Documentation Requirements

### Architecture Decision Records (ADRs)
- Document significant architectural decisions
- Include: context, decision, consequences
- Update ADRs when decisions change
- Keep ADRs accessible to team

### System Documentation
- High-level architecture diagrams
- Component interaction diagrams
- Data flow diagrams
- Deployment architecture
- Failure modes and recovery

### API Documentation
- OpenAPI/Swagger for REST APIs
- Protocol buffer definitions for gRPC
- Message schemas for async communication
- Versioning strategy
- Error handling documentation

## Integration Patterns

### Service Communication
- Choose appropriate communication patterns (sync/async)
- Design for failure (circuit breakers, retries, timeouts)
- Use appropriate protocols (HTTP, gRPC, message queues)
- Document communication contracts
- Plan for versioning

### Data Integration
- Design data pipelines carefully
- Consider data consistency
- Plan for data transformation
- Document data schemas
- Design for data quality

### External Dependencies
- Minimize external dependencies
- Document dependency rationale
- Plan for dependency failures
- Version external dependencies
- Monitor dependency health

## Performance and Scalability

### Performance Considerations
- Identify performance bottlenecks
- Design for expected load
- Plan for capacity scaling
- Consider caching strategies
- Monitor performance metrics

### Scalability Design
- Design for horizontal scaling
- Avoid single points of failure
- Design stateless services when possible
- Plan for data partitioning
- Consider eventual consistency

## Security
- Design with security in mind
- Follow principle of least privilege
- Encrypt sensitive data
- Validate all inputs
- Document security considerations
