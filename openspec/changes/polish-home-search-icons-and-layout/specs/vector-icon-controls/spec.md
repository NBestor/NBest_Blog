## ADDED Requirements

### Requirement: Vector icon controls
The system SHALL render key action controls with local vector icons instead of plain symbol text, while preserving accessible labels.

#### Scenario: Search entry uses a vector icon
- **WHEN** the user views the top navigation search entry
- **THEN** the search control MUST display a vector magnifier icon with an accessible search label

#### Scenario: Like button uses heart states
- **WHEN** content is not liked by the current user
- **THEN** the like control MUST display an outline heart icon

#### Scenario: Liked button uses filled red heart
- **WHEN** content is liked by the current user
- **THEN** the like control MUST display a filled red heart icon

#### Scenario: Calendar expansion uses vector arrow
- **WHEN** the home calendar event drawer can be expanded or collapsed
- **THEN** the drawer toggle MUST display a vector arrow icon that communicates the current direction

