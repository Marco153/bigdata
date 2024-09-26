import pickle
import imgui
from PIL import Image
from imgui.integrations.glfw import GlfwRenderer
import glfw
from OpenGL.GL import *
import numpy as np

# Initialize GLFW for window creation
if not glfw.init():
    print("Could not initialize GLFW")
    exit(1)

width = 800
height = 600
window = glfw.create_window(width, height, "PyImGui Example", None, None)
if not window:
    glfw.terminate()
    print("Could not create window")
    exit(1)

# Make the OpenGL context current
glfw.make_context_current(window)

# Set up Dear ImGui context
imgui.create_context()
impl = GlfwRenderer(window)

# Application state variables
show_demo_window = True
text_input_value = ""
senha_value = ""
checkbox_state = False

def create_texture(image_path):
    # Load the image using PIL (Pillow)
    image = Image.open(image_path)
    #image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image for OpenGL's coordinate system
    img_data = image.convert("RGBA").tobytes()  # Convert image to RGBA and get the byte data
    width, height = image.size

    # Generate a texture ID
    texture_id = glGenTextures(1)

    # Bind the texture to apply subsequent settings
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Define the texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Minification filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Magnification filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  # Wrap mode for S axis
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)  # Wrap mode for T axis

    # Upload the texture data to OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    # Generate mipmaps (optional for better texture quality when scaling down)
    glGenerateMipmap(GL_TEXTURE_2D)

    # Unbind the texture to avoid unintentional modifications
    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id	


#logo = create_texture("logo.jpg")

style = imgui.get_style()
style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.6, 0.5, 0.8, 1.0) 
page = 0


io = imgui.get_io()

new_font = io.fonts.add_font_from_file_ttf(
    "arial.ttf", 20,
)
impl.refresh_font_texture()

langs = {}

with open("langs.json", 'rb') as lang_file:
	langs = pickle.load(lang_file)


def GetLangArray(lang_name, months):
	lang_ar_ = langs[lang_name]
	total_samples = int((8 * 12) / months)
	lang_ar_ret = np.arange(0.0, total_samples)

	for i in range(0, total_samples):
		sl = lang_ar_[i * months: i * months + months]
		if np.sum(sl) != 0:
			lang_ar_ret[i] = np.average(sl)
		else:
			lang_ar_ret[i] = 0


	lang_ar_ = map(lambda pair:(40 + pair[0] * 10, -pair[1] * 10 + 400), enumerate(lang_ar_ret))
	lang_ar_ = list(lang_ar_)
	return lang_ar_




#lang_ar = GetLangArray("TypeScript", 2)

#print(langs)
to_pick_langs_selected = [0] * len(langs)
langs_selected = dict()
#print(lang_ar_pos)


# Main application loop
while not glfw.window_should_close(window):
	glfw.poll_events()
	impl.process_inputs()

    # Start a new ImGui fram
	imgui.new_frame()

	imgui.set_next_window_position(0, 0)
	imgui.set_next_window_size(width, height)

    # Create a new fullscreen window
	imgui.begin("Fullscreen UI Window", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE)

	imgui.begin_child("langs region", 150, 150)
	imgui.push_style_color(imgui.COLOR_HEADER_ACTIVE, *imgui.Vec4(0.5, 0.0, 0.0, 1.0))  # Red color
	#imgui.push_style_color(imgui.COLOR_HEADER, *imgui.Vec4(0.4, 0.6, 0.0, 1.0))  # Red color


	for i, lng in enumerate(langs.keys()):
		clicked, to_pick_langs_selected[i] = imgui.selectable(str(lng), to_pick_langs_selected[i])
		if clicked:
			print("new lang")
			#print(list(langs)[i])
			langs_selected[str(lng)] = {'ar': GetLangArray(str(lng), 2), 'color': (1.0, 0.0, 0.0, 1.0)}



	#imgui.pop_style_color()
	imgui.pop_style_color()
	imgui.end_child()

	imgui.same_line()

	imgui.begin_child("selected langs", 200, 150)
	for i, lng in enumerate(langs.keys()):
		if to_pick_langs_selected[i] == 1:
			#print("selected")
			imgui.text(str(lng))
			imgui.same_line()
			_, langs_selected[lng]['color'] = imgui.color_edit4(f"##picker{i}", *langs_selected[lng]['color'])

	imgui.end_child()

	langs
	draw_list = imgui.get_window_draw_list()

	# printing lines
	for lng in langs_selected:
		#print(langs_selected[str(lng)])
		draw_list.add_polyline(langs_selected[lng]['ar'], imgui.get_color_u32_rgba(*langs_selected[lng]['color']), flags=imgui.DRAW_NONE, thickness=3)

	imgui.push_font(new_font)
	'''
	if page == 0:
		Login()
	elif page == 1:
		AlunoPanel()
	elif page == 2:
		ProfessorPanel()
	'''
	imgui.pop_font()

    # End the UI window
	imgui.end()

    # OpenGL rendering
	glClearColor(0.1, 0.1, 0.1, 1)
	glClear(GL_COLOR_BUFFER_BIT)

    # Render the ImGui frame
	imgui.render()
	impl.render(imgui.get_draw_data())

    # Swap buffers
	glfw.swap_buffers(window)

# Cleanup
impl.shutdown()
glfw.terminate()
