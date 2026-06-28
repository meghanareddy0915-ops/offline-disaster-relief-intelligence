# Offline Disaster Relief Intelligence System

## Overview

The Offline Disaster Relief Intelligence System is a CPU-first, offline-first AI application that helps emergency responders process disaster relief requests without requiring an internet connection.

The application accepts unstructured inputs such as text, images, and PDF documents. It extracts important information using OCR and a local language model, converts the information into structured data, and stores it in a local SQLite database for quick retrieval.

## Problem Statement

During natural disasters, relief requests arrive in different formats including handwritten notes, scanned forms, and text messages. Organizing these requests manually is time-consuming and can delay rescue operations, especially in areas with poor internet connectivity.

## Solution

This project provides an offline AI-powered solution that automatically extracts important information from disaster requests and converts it into structured records.

## Features

* Offline-first AI processing
* CPU-only inference
* OCR-based text extraction
* Local Language Model (LLM)
* Structured JSON generation
* SQLite database storage
* Search and filtering of requests
* Priority classification

## Technology Stack

### Frontend

* React
* Vite

### Backend

* FastAPI

### OCR

* Tesseract OCR

### Local AI

* llama.cpp
* Gemma 3 1B GGUF (or TinyLlama)

### Database

* SQLite

## Project Workflow

1. Upload Text, Image or PDF.
2. Extract text using OCR.
3. Process the extracted text using a local AI model.
4. Convert the information into structured JSON.
5. Store the structured data in SQLite.
6. Display searchable disaster requests.

## Team Members

### Member 1

* Documentation
* Frontend Development
* UI Design
* Testing

### Member 2

* Backend Development
* OCR Integration
* Local AI Integration
* Database Management

## Future Enhancements

* Voice input support
* Offline map integration
* Multi-language support
* Mobile application
* Disaster analytics dashboard

## License

This project is licensed under the GPL-3.0 License.