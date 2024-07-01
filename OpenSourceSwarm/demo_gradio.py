import time


def demo_gradio(agency, height=450, dark_mode=True):
    """
    Launches a Gradio-based demo interface for the agency chatbot.

    Parameters:
        height (int, optional): The height of the chatbot widget in the Gradio interface. Default is 600.
        dark_mode (bool, optional): Flag to determine if the interface should be displayed in dark mode. Default is True.
        share (bool, optional): Flag to determine if the interface should be shared publicly. Default is False.
    This method sets up and runs a Gradio interface, allowing users to interact with the agency's chatbot. It includes a text input for the user's messages and a chatbot interface for displaying the conversation. The method handles user input and chatbot responses, updating the interface dynamically.
    """
    try:
        import gradio as gr
    except ImportError:
        raise Exception("Please install gradio: pip install gradio")

    js = """function () {
      gradioURL = window.location.href
      if (!gradioURL.endsWith('?__theme={theme}')) {
        window.location.replace(gradioURL + '?__theme={theme}');
      }
    }"""

    if dark_mode:
        js = js.replace("{theme}", "dark")
    else:
        js = js.replace("{theme}", "light")

    message_file_ids = []
    message_file_names = None
    recipient_agents = [agent.name for agent in agency.main_recipients]
    recipient_agent = agency.main_recipients[0]

    with (gr.Blocks(js=js) as demo):
        chatbot = gr.Chatbot(height=height)
        with gr.Row():
            with gr.Column(scale=9):
                dropdown = gr.Dropdown(label="Recipient Agent", choices=recipient_agents,
                                       value=recipient_agent.name)
                msg = gr.Textbox(label="Your Message", lines=4)
            with gr.Column(scale=1):
                file_upload = gr.Files(label="Files", type="filepath")
        button = gr.Button(value="Send", variant="primary")

        def handle_dropdown_change(selected_option):
            nonlocal recipient_agent
            recipient_agent = agency._get_agent_by_name(selected_option)

        def handle_file_upload(file_list):
            nonlocal message_file_ids
            nonlocal message_file_names
            message_file_ids = []
            message_file_names = []
            if file_list:
                try:
                    for file_obj in file_list:
                        with open(file_obj.name, 'rb') as f:
                            # Upload the file to OpenAI
                            file = agency.main_thread.client.files.create(
                                file=f,
                                purpose="assistants"
                            )
                        message_file_ids.append(file.id)
                        message_file_names.append(file.filename)
                        print(f"Uploaded file ID: {file.id}")
                    return message_file_ids
                except Exception as e:
                    print(f"Error: {e}")
                    return str(e)

            return "No files uploaded"

        def user(user_message, history):
            if not user_message:
                return user_message, history

            if history is None:
                history = []

            original_user_message = user_message

            # Append the user message with a placeholder for bot response
            if recipient_agent:
                user_message = f"👤 User @{recipient_agent.name}:\n" + user_message.strip()
            else:
                user_message = f"👤 User:" + user_message.strip()

            nonlocal message_file_names
            if message_file_names:
                user_message += "\n\n:paperclip: Files:\n" + "\n".join(message_file_names)

            return original_user_message, history + [[user_message, None]]

        def bot(original_message, history):
            nonlocal message_file_ids
            nonlocal message_file_names
            nonlocal recipient_agent
            print("Message files: ", message_file_ids)
            # Replace this with your actual chatbot logic
            gen = agency.get_completion(message=original_message, message_files=message_file_ids,
                                        recipient_agent=recipient_agent, yield_messages=True)

            message_file_ids = []
            message_file_names = []
            try:
                # Yield each message from the generator
                for bot_message in gen:
                    if bot_message.sender_name.lower() == "user":
                        continue

                    # sometimes thread stops before bot message is received
                    if not bot_message.content:
                        main_thread = agency.main_thread
                        content = bot_message.content
                        num_attempts = 0
                        while not content or num_attempts < 30:
                            time.sleep(1)
                            content = main_thread._get_last_message_text()
                            num_attempts += 1

                        bot_message.content = content

                    message = bot_message.get_formatted_content()

                    history.append((None, message))
                    yield "", history
            except StopIteration:
                # Handle the end of the conversation if necessary
                pass

        button.click(
            user,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        ).then(
            bot, [msg, chatbot], [msg, chatbot]
        )
        dropdown.change(handle_dropdown_change, dropdown)
        file_upload.change(handle_file_upload, file_upload)
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, [msg, chatbot], [msg, chatbot]
        )

        # Enable queuing for streaming intermediate outputs
        demo.queue()

    # Launch the demo
    demo.launch(share=False, debug=True)
    return demo