import pypdfium2 as pdfium
from io import BytesIO
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Image,
    HarmCategory,
    HarmBlockThreshold,
)

multimodal_model = GenerativeModel("gemini-1.5-pro")

def describe_image(image_byte_array, caption_file_name):
    prompt = """You are a very professional document summarization specialist. Given a document, your task is to understand the concept and explain in detail and provide a detailed summary of the content of the document.
    If it includes images, provide descriptions of the images.
    If it includes tables, extract all elements of the tables.
    If it includes graphs, explain the findings in the graphs.
    If it includes mathematical formula, understand and explain so that we are able to solve the problems that user may ask later.
    If it includes flowcharts, understand and provide descriptions of the flowcharts.
    """
    image_data = Image.from_bytes(image_byte_array)
    contents = [image_data, prompt]

    config = GenerationConfig(max_output_tokens=4096,temperature=0.0)

    safety_config = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    try:    
        responses = multimodal_model.generate_content(contents, generation_config=config, stream=False,safety_settings=safety_config)
    except ValueError as e:
        print(f"Something went wrong with the API call: {e}")
        # If the response doesn't contain text, check if the prompt was blocked.
        print(responses.prompt_feedback)
        # Also check the finish reason to see if the response was blocked.
        print(responses.candidates[0].finish_reason)
        # If the finish reason was SAFETY, the safety ratings have more details.
        print(responses.candidates[0].safety_ratings)
        raise Exception(f"Something went wrong with the API call: {e}")

    #messages = ""
    #for response in responses:
    #    print(response.text, end="")
   #     messages = messages + response.text
    msg=responses.text
    print(f"Filename : {caption_file_name} Enriched text: {msg}")

    with open(caption_file_name, "w") as text_file:
        print(msg, file=text_file)

def convert_pdf_to_images(file_path, scale=300/72):
    
    pdf_file = pdfium.PdfDocument(file_path)  
    page_indices = [i for i in range(len(pdf_file))]
    
    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices = page_indices, 
        scale = scale,
    )
    
    list_final_images = [] 
    
    for i, image in zip(page_indices, renderer):
        
        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_file_name = f"images/standard-chartered-plc-full-year-2023-report_{i}.jpg"
        caption_file_name = f"captions/standard-chartered-plc-full-year-2023-report_{i}.txt"
        image.save(image_file_name, 'jpeg' )
        image_byte_array = image_byte_array.getvalue()
        describe_image(image_byte_array,caption_file_name)
        list_final_images.append(dict({i:image_byte_array}))
    
    return list_final_images


convert_pdf_to_images = convert_pdf_to_images('standard-chartered-plc-full-year-2023-report.pdf')
print("Completed Storing images")


