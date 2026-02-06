🧠 AI Smart Exam Evaluator System

    An interactive AI-powered exam platform built using **Streamlit + Groq LLM**, where users can generate custom tests, attend them, and receive detailed evaluations with explanations.
    This system dynamically creates questions based on user preferences and provides instant scoring, explanations, and improvement areas.

🚀 Features

    * Generate exams by:
        * Topic
        * Exam type (GATE / Placements / College / etc.)
        * Difficulty level (Easy / Medium / Hard)
        * Question type (MCQ / Fillups / Mixed)
        * Number of questions

    * AI automatically:

        * Creates questions
        * Generates real answer options (not A/B/C/D)
        * Stores correct answers internally
        * Shuffles options

    * User can:

        * Attend the test
        * Submit answers
        * View score instantly

    * After submission:

        * Shows **user answer**
        * Shows **correct answer**
        * Gives **simple explanations for every question**
        * Highlights **wrong answers**
        * Displays **focus / improvement areas**

🛠 Tech Stack

    * Python
    * Streamlit (UI)
    * Groq LLM (Question generation + evaluation)
    * python-dotenv

\📦 Requirements

    Create a `requirements.txt` with:

    ```
      streamlit
      groq
      python-dotenv
    ```



## 📂 Project Structure

```
.
├── app2.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

🎯 Learning Outcomes

    * Prompt engineering
    * LLM integration  
    * Streamlit UI design
    * JSON handling from AI
    * Evaluation logic
    * Building real AI applications



