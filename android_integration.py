# Show how it integrates with Android
android_code = """
// MainActivity.kt - Simplified Android integration
class TriageActivity : AppCompatActivity() {
    fun processSymptomOffline(audioPath: String) {
        // 1. Load quantized Whisper
        val whisper = Interpreter(loadModel("whisper_4bit.tflite"))
        
        // 2. Transcribe offline
        val text = whisper.transcribe(audioPath)
        
        // 3. Load quantized Llama
        val llama = Interpreter(loadModel("llama3_4bit.tflite"))
        
        // 4. Extract symptoms
        val symptoms = llama.extract(text)
        
        // 5. Apply medical rules
        val result = MedicalRules.evaluate(symptoms)
        
        // 6. Show result - 100% offline
        showTriageResult(result)
    }
}
"""