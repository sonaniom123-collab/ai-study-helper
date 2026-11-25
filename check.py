from core.code_templates import get_code
from core.intent import detect_language, predict_operation
q = "બે સંખ્યાનો ભાગાકાર"
label = predict_operation(q)
language = detect_language(q)
print("label:", label)
print("language:", language)
print(get_code(label, language))
