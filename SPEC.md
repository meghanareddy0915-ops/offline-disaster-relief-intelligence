# Project Specification

## Project Name
Offline Disaster Relief Intelligence System

## Hackathon Theme
CPU-First and Offline-First AI

---

## Objective

To develop an offline AI application that converts unstructured disaster relief requests into structured data using CPU-based open-source AI models without requiring an internet connection.

---

## Problem Statement

During disasters such as floods, earthquakes, cyclones, and landslides, relief requests are received in various formats including text, scanned documents, and images. Manually processing these requests is slow and can delay emergency response. The proposed system automates the extraction and organization of critical information while operating completely offline.

---

## Target Users

- Disaster Response Teams
- NGOs
- Government Agencies
- Emergency Volunteers

---

## Input

The system accepts the following inputs:

- Text
- Images (.jpg, .png)
- PDF documents

---

## Processing Workflow

1. User uploads a text, image, or PDF.
2. OCR extracts text from images or scanned documents.
3. A local language model processes the extracted text.
4. Important information is identified.
5. Structured JSON is generated.
6. Data is stored in SQLite.
7. Users can search and view previous requests.

---

## Output Fields

- Disaster Type
- Location
- Number of People Affected
- Resources Required
- Priority Level
- Status

---

## Functional Requirements

- Upload disaster requests
- OCR text extraction
- Local AI processing
- JSON generation
- SQLite storage
- Search requests
- Display structured results

---

## Non-Functional Requirements

- Offline-first
- CPU-only execution
- Lightweight
- Fast response time
- Open-source software

---

## Technology Stack

### Frontend
- React
- Vite

### Backend
- FastAPI

### Database
- SQLite

### OCR
- Tesseract OCR

### Local AI
- llama.cpp
- Gemma 3 1B GGUF

---

## Future Scope

- Voice message support
- Multi-language processing
- Offline maps
- Resource allocation dashboard
- Mobile application
