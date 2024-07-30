import presets
from app import render_prompt
import gradio as gr





js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'Stable Diffusion Simple UI';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

css = """
#filler-row {
    min-height: 70px; 
}
#short-row {
    height: 20px; 
    overflow: hidden;  /* This prevents content from spilling out */
}
.sticky-element {
    position: fixed;
    top: 280;  /*value to change where it sticks */
    z-index: 1000;  /* Ensure it stays on top of other elements */
}
.image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 400px;  
    width: 472px;   
    overflow: hidden;
    background-color: #202c3c;  /* colour*/
}
.image-container img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
"""

presets_list = list(presets.presets.keys())
material_list = list(presets.materials.keys())
checkpoint_list = ["test", "test"]
preprocessor_list = ["test", "t"]

def get_attributes(list):
    if list:
        prompt = [presets.presets[e] for e in list if e in presets.presets]
        return prompt
    else:
        return []

def get_materials(list):
    if list:
        prompt = [presets.materials[e] for e in list if e in presets.materials]
        return prompt
    else:
        return []

def generate_image(
                matlist, 
                attlist, 
                b, 
                text, 
                negative_prompt="",
                num_steps=5,
                g_scale=1,
                height=500,
                width=500,
                img=None
                ):
    
    prompt = ",".join(get_attributes(attlist) + get_materials(matlist))
    if b:
        prompt += "," + text if prompt else text
        



    return render_prompt(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_steps=num_steps,
        g_scale=g_scale,
        height=height,
        width=width,
        img=img
        )

def toggle_prompt(b):
    return gr.update(visible=b)

def get_image_dimensions(s1, s2):
    return str(s1) + "x" + str(s2)

theme = gr.themes.Soft(
    primary_hue="sky",
    secondary_hue="blue",
    neutral_hue="slate",
    )

with gr.Blocks(js=js, css=css, theme=theme) as demo:

    with gr.Row():

        with gr.Column(scale=1):
                
            #checkpoint

            with gr.Row(elem_id="short-row"):

                gr.Markdown("SD checkpoint")

            with gr.Row(): 

                checkpoint = gr.Dropdown(checkpoint_list, scale=0, label="SD checkpoint", container=False)

            #Checkboxes

            with gr.Row():

                promptCheckbox = gr.Checkbox(label="Include manual prompt", value=False, scale=0, min_width=200, container=False)
                useImageCheckbox = gr.Checkbox(label="Include image reference", scale=0, min_width=200, container=False)
            
            #Prompt box

            with gr.Row():

                promptTextbox = gr.Textbox(placeholder="Enter your prompt", show_label=False, min_width=500, visible=False, interactive=True)
                promptCheckbox.change(fn=toggle_prompt, inputs=promptCheckbox, outputs=promptTextbox)

            #Image size

            with gr.Group():

                with gr.Row():

                    imageW = gr.Slider(minimum=104, maximum=3000, step=8, label="Image Width")

                with gr.Row():

                    imageH = gr.Slider(minimum=104, maximum=3000, step=8, label="Image Height")
                    
                #Image dimensions label
                #with gr.Row():
                    
                    #dimensions = gr.Markdown("1000x1000")
                    #Update dimensions
                    #imageH.change(fn=get_image_dimensions, inputs=[imageW, imageH], outputs=dimensions, show_progress=False)
                    #imageW.change(fn=get_image_dimensions, inputs=[imageW, imageH], outputs=dimensions, show_progress=False)

            #CN image

            CNImageH = 400
            CNImageW = 448

            with gr.Row():

                with gr.Group(visible=False) as tabsContainer:

                    with gr.Tabs():

                        with gr.TabItem("Image unit 1"):
                                        
                            CNUnit1 = gr.Image(width=CNImageW, height=CNImageH)
                            gr.Markdown("Preprocessor:")
                            preProc1 = gr.Dropdown(preprocessor_list, container=False, scale=0)
                        
                        with gr.TabItem("Image unit 2"):

                            CNUnit2 = gr.Image(width=CNImageW, height=CNImageH)
                            gr.Markdown("Preprocessor:")
                            preProc2 = gr.Dropdown(preprocessor_list, container=False, scale=0)                           
                        
                        with gr.TabItem("Image unit 3"):

                            CNUnit3 = gr.Image(width=CNImageW, height=CNImageH)
                            gr.Markdown("Preprocessor:")
                            preProc3 = gr.Dropdown(preprocessor_list, container=False, scale=0)
                
                useImageCheckbox.change(fn=toggle_prompt, inputs=useImageCheckbox, outputs=tabsContainer)
                            


            



    
        with gr.Column():

            with gr.Row(elem_id="filler-row"):
                pass
            with gr.Row():

                generate = gr.Button("Generate", scale=0)
                
            with gr.Row():

                with gr.Group():

                    outputImage = gr.Image(value = r"C:\UI test\output\2024-07-23_11-18.png", elem_classes="image-container")


            #Presets

            with gr.Row():

                promptPresets = gr.Dropdown(presets_list, multiselect=True, scale=0, min_width=500, info="Select attributes for the image", label="")


            with gr.Row():

                materialPresets = gr.Dropdown(material_list, multiselect=True, scale=0, min_width=500, info="Select materials for the image", label="")


    generate.click(
    fn=lambda material_preset, prompt_preset, prompt_checkbox, prompt_text, h, w, img: 
        generate_image(
            matlist=material_preset, 
            attlist=prompt_preset, 
            b=prompt_checkbox, 
            text=prompt_text, 
            height=h, 
            width=w,
            img=img
        ),
    inputs=[
        materialPresets,
        promptPresets,
        promptCheckbox,
        promptTextbox,
        imageH,
        imageW,
        CNUnit1
        ], 
        outputs=outputImage
    )



demo.launch(show_api=False)

