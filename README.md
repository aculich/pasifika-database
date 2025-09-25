# Pasifika Project Charter (Draft)

## Project Overview

The Pasifika Project is creating an open, community-serving platform that connects Pacific Island filmmakers and scholars through a searchable directory, rich film records, and integrated geospatial context. The platform will surface films, directors, places, and languages on an interactive map and enable respectful, verifiable community contributions aligned with FAIR and CARE principles.

## Purpose and Problem Statement

- Fragmented information about Pacific Island films and filmmakers makes discovery and collaboration difficult.
- Existing data structures and tools have grown organically, creating schema complexity and operational friction.
- Geospatial context is essential but currently hard to access and integrate.

This project will provide a cohesive, sustainable, and extensible platform to improve discoverability, collaboration, and research, while honoring cultural data governance.

## Goals and Objectives

- Build an interactive public website for film discovery with map-based exploration.
- Provide a directory of filmmakers with controlled contact sharing and consent-aware workflows.
- Enable community submissions with automated validity checks before publication.
- Publish open datasets and downloads for films and island data with clear provenance.
- Implement FAIR and CARE principles from the start for ethical, reusable, and community-aligned data.

## Primary Audiences

- Pacific Island filmmakers seeking peers and collaborators.
- Scholars of Pacific Island filmmaking and geography.

## Scope and Deliverables

- Single public site with distinct sections: Films and Geospatial Downloads
- Public website with search, browse, and map interaction for films, directors, islands, and languages.
- Data model and relational schema for films, people, places, and metadata.
- Contribution pipeline with automated validation and moderation controls.
- Exports and APIs for open access to appropriate datasets.
- Operational playbook and technical architecture for hosting and maintenance.

## Success Criteria

- Films and directors can be found via robust search and map filters.
- Community submissions pass automated checks and are published promptly.
- Data downloads and documentation meet FAIR guidelines and CARE considerations.
- Clear governance and sustainability plan for data stewardship and hosting.

## Principles and Constraints

- FAIR and CARE principles guide all data practices.
- Open-source approach when possible, with respect for cultural sensitivities.
- Cost-aware, scalable hosting and data pipelines.
- Accessibility and usability for non-technical audiences.

## Initial Technical Stack (working list)

- Data: Airtable source exports, Postgres, ERD analysis and normalization.
- Mapping: Leaflet or Mapbox for interactive layers, USGS Small Islands dataset, Global Islands and Centroids.
- Web: React frontend, Django exploration, potential API layer.
- DevOps: Docker for containerization, GitHub for version control, Zoom and Notion for collaboration.

## Immediate Next Steps

- Inventory current tools and credentials. Export Airtable tables for ingestion.
- Finalize proposed relational schema and migrate representative sample.
- Stand up a minimal map with film markers to validate end-to-end flow.
- Draft contribution workflow and automated validation rules.

---

### Historical Project Notes

- Two-year project history clarified. Current focus is the Pacifica Geographies drive with ~10GB of data.
- Prior schema import to SQL revealed normalization needs and duplicate columns; ERD work underway.
- Vision: map-centric site with film pages, director directory, downloads, and contribution flow.
- Target audiences: filmmakers and scholars. Prior work on ocean-current base map provides cultural and visual context.
- Action items include emailing faculty about FAIR and CARE, sharing Airtable access, and deciding on one combined site vs adjacent sites.