from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from fastapi import FastAPI
import os
import bittensor as bt

os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_ORGANIZATION"] = "org-THx9POZUskofWSI3F86rf3as"

llm = OpenAI(model_name="text-davinci-003")



def request_toc_openai(str_toc_prompt):
    template = "{question}"
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    response = llm_chain.run(str_toc_prompt)
    print(response)
    return response

def request_toc_bittensor(str_toc_prompt, uid):
    wallet = bt.wallet() # Your validator wallet.
    metagraph = bt.metagraph( netuid = 1 ) # Get state from subnetwork 1.
    dendrite = bt.text_prompting( keypair = wallet.hotkey, 
                                  axon = metagraph.axons[ uid ] ) # Connection to uid 
    subnet_response = dendrite.forward( roles = ['system', 'user'], 
                      messages = ['you write wikipedia pages and specifically create the table of contents for any given page', str_toc_prompt] ) 
    # Check response for subnet_response.return_message to make sure it is a success
    if subnet_response.return_message.lower() != "success":
        return "FAILURE"


    final_subnet_response = subnet_response.completion
    if "conclusion" not in subnet_response.completion.lower():
        counter = 1
        str_toc_prompt += " Continue this beginning of a table of contents: "
        while conclusion not in subnet_response.completion.lower() and counter < 5:
            str_toc_prompt += subnet_response.completion
            counter += 1
            subnet_response = dendrite.forward( roles = ['system', 'user'], 
                                                messages = ['you write wikipedia pages and specifically create the table of contents for any given page', str_toc_prompt] ) 
            final_subnet_response += subnet_response.completion
        if counter == 5:
            # we need to cut it off and add a conclusion
            final_subnet_response += "\n999. Conclusion"

    print(final_subnet_response)
    return final_subnet_response

def generate_toc_content_openai(prompts):
    template = "{question}"
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    toc_response_ls = []
    for prompt in prompts:
        response = llm_chain.run(prompt)
        toc_response_ls.append(response)
        print(f"Prompt: {prompt} \n Response: \n {response} \n \n")
    return toc_response_ls

def generate_toc_content_bittensor(prompts, topic, uid):
    wallet = bt.wallet() # Your validator wallet.
    metagraph = bt.metagraph( netuid = 1 ) # Get state from subnetwork 1.
    dendrite = bt.text_prompting( keypair = wallet.hotkey, 
                                  axon = metagraph.axons[ uid ] ) # Connection to uid 
    system_role = f"you write wikipedia pages, you are currently writing the sections for the page on the topic '{topic}'"
    
    toc_response_ls = []
    for prompt in prompts:
        subnet_response = dendrite.forward( roles = ['system', 'user'], 
                                                messages = [system_role, prompt] ) 
        toc_response_ls.append(subnet_response)
        print(f"Prompt: {prompt} \n Response: \n {subnet_response} \n \n")
    return toc_response_ls
