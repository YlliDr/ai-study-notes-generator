# AI-Powered Study Notes Generator Using Seq2Seq Transformers

## Project Description

This project is an NLP web application that converts long text into useful study material. The user can paste an article, lecture note, or textbook section, and the system generates a summary, key points, flashcards, quiz questions, topic label, and difficulty level.

The project uses transformer-based sequence-to-sequence models from Hugging Face. Summarization is performed using a DistilBART model, while flashcards and quiz questions are generated using FLAN-T5.

## Main Features

- Text preprocessing
- Abstractive summarization
- Key point generation
- Flashcard generation
- Quiz question generation
- Topic classification
- Difficulty classification
- Downloadable study notes

## Technologies Used

- Python
- Streamlit
- Hugging Face Transformers
- PyTorch
- Scikit-learn
- Pandas

## NLP Methods Used

### Text Preprocessing

The input text is cleaned by removing unnecessary spaces and line breaks. Long text is split into smaller chunks so it can be processed by transformer models.

### Seq2Seq Summarization

The project uses a transformer-based summarization model. The model receives a long text sequence as input and generates a shorter summary sequence as output.

### Text-to-Text Generation

FLAN-T5 is used to generate key points, flashcards, and quiz questions. T5 treats NLP tasks as text-to-text problems, where both the input and output are text.

### Zero-Shot Classification

The app classifies the text topic and difficulty level using a pretrained zero-shot classification model.

## Project Pipeline

Input Text → Preprocessing → Chunking → Summarization → Generation → Classification → Study Notes Output

## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-study-notes-generator.git
cd ai-study-notes-generator