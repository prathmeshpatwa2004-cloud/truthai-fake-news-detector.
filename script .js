const API_URL = "https://YOUR-BACKEND.onrender.com";

let marathiMode = false;

function toggleLanguage() {
  marathiMode = !marathiMode;

  document.getElementById("languageButton").textContent =
    marathiMode ? "English" : "मराठी";

  document.getElementById("heading").textContent =
    marathiMode ? "बातमी तपासा" : "Check Your News";

  document.getElementById("instructions").textContent =
    marathiMode
      ? "खाली बातमीचे शीर्षक किंवा संपूर्ण बातमी टाका."
      : "Paste a news headline or article below.";

  document.getElementById("newsInput").placeholder =
    marathiMode
      ? "मराठी किंवा इंग्रजी बातमी येथे टाका..."
      : "Enter English or Marathi news...";

  document.getElementById("checkButton").textContent =
    marathiMode ? "🤖 बातमीचे विश्लेषण करा" : "🤖 Analyse News";

  document.getElementById("clearButton").textContent =
    marathiMode ? "पुसून टाका" : "Clear";
}

async function checkNews() {
  const news = document.getElementById("newsInput").value.trim();
  const button = document.getElementById("checkButton");
  const status = document.getElementById("status");
  const result = document.getElementById("result");

  result.hidden = true;
  status.textContent = "";

  if (news.length < 20) {
    status.textContent = marathiMode
      ? "कृपया किमान 20 अक्षरांची बातमी टाका."
      : "Please enter at least 20 characters of news.";
    return;
  }

  button.disabled = true;
  status.textContent = marathiMode
    ? "बातमीचे विश्लेषण सुरू आहे..."
    : "Analysing news...";

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: news })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Analysis failed.");
    }

    document.getElementById("resultHeading").textContent =
      marathiMode ? "विश्लेषणाचा निकाल" : "Analysis Result";

    document.getElementById("prediction").textContent =
      (marathiMode ? "निकाल: " : "Result: ") + data.label;

    document.getElementById("explanation").textContent =
      data.explanation;

    result.hidden = false;
    status.textContent = "";
  } catch (error) {
    status.textContent = marathiMode
      ? "सर्व्हरशी संपर्क झाला नाही. बॅकएंड URL आणि सर्व्हर तपासा."
      : "Could not connect to the server. Check your backend URL and server.";
  } finally {
    button.disabled = false;
  }
}

function clearNews() {
  document.getElementById("newsInput").value = "";
  document.getElementById("status").textContent = "";
  document.getElementById("result").hidden = true;
      }
