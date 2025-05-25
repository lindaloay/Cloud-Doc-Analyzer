def classify_document(text):
    text = text.lower()
    if "تقرير" in text or "بحث" in text:
        return "تقرير"
    elif "مقال" in text or "رأي" in text:
        return "مقال"
    elif "فاتورة" in text or "سعر" in text or "مبلغ" in text:
        return "مالي"
    else:
        return "غير معروف"
