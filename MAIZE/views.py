from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import numpy as np
import tensorflow as tf

# Correct the path to point to the directory containing 'saved_model.pb'
model_path = r'C:\Users\user\Desktop\PROJECT\maize_disease_detection\MAIZE\model'
model = tf.saved_model.load(model_path)

# Define your classes
classes = ['Common Rust', 'Blight', 'Gray Leaf Spot', 'Healthy']

# Define recommendations for each class
recommendations = {
    'Common Rust': 'Pendekezo: Tumia dawa za kuulia wadudu kama vile Mancozeb ili kupunguza uharibifu wa majani.',
    'Blight': 'Pendekezo: Tumia dawa za kuulia wadudu kama vile Dithane M-45 ili kudhibiti kuenea kwa ugonjwa huu.',
    'Gray Leaf Spot': 'Pendekezo: Tumia dawa za kuulia wadudu kama vile Quadris na fanya mzunguko wa mazao ili kudhibiti ugonjwa huu.',
    'Healthy': 'Mahindi yako ni yenye afya. Hakuna hatua za ziada zinazohitajika kwa sasa.'
}

@csrf_exempt
def predict_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_path = default_storage.save(image.name, ContentFile(image.read()))
        image_full_path = os.path.join(settings.MEDIA_ROOT, image_path)

        # Preprocess the image
        img = tf.keras.preprocessing.image.load_img(image_full_path, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        # Make prediction
        infer = model.signatures['serving_default']
        predictions = infer(tf.convert_to_tensor(img_array))
        predictions = predictions['dense_1']  # Use the correct key

        predicted_class = classes[np.argmax(predictions[0])]
        confidence = float(np.max(predictions[0]))  # Convert to Python float

        # Construct the guidance message with recommendations
        guidance_message = recommendations.get(predicted_class, 'Hali ya mmea haijulikani.')

        response_data = {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'guidance_message': guidance_message,
        }

        # Clean up
        default_storage.delete(image_path)

        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
