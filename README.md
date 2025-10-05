# Personalized-AI-Chatbot
An end-to-end AI assistant with Retrieval-Augmented Generation, designed for seamless integration with other projects.

<p style="display: flex; justify-content: space-between;">
  <img src="screenshots/chatbot_1.png" style="width: 32%;" />
  <img src="screenshots/chatbot_2.png" style="width: 32%;" />
  <img src="screenshots/chatbot_3.png" style="width: 32%;" />
</p>



## Project structure
```
Personalized-AI-Chatbot/
├── backend/
│   ├── main.py
│   ├── utils.py
│   ├── rag_pipeline.py
│   └── requirements.txt
├── data/
│   └── docs/
│       └── ...                     # Your documents for RAG (txt, pdf, doc, html)
├── frontend/
│   ├── public/
│   ├── src/components/AIChatWindow/
│   │   ├── AIChatWindow.tsx
│   │   └── AIChatLoader.tsx
│   ├── hooks/
│   │   └── useAIChat.ts
│   ├── styles/
│   │   │   AIChatLoader.css
│   │   └── AIChatWindow.css
│   └── main.tsx
├── llm-models/
│   └── ...                         # Your local LLM models
├── screenshots/
├── .gitignore
├── LICENSE
├── README.md
└── docker-compose.yml

```

## License

Personalized-AI-Chatbot is released under the MIT license.

## Author

Sebastian Brzustowicz &lt;Se.Brzustowicz@gmail.com&gt;
