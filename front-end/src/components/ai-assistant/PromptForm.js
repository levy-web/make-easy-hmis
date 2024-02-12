import React, { useState } from 'react'
import { toast } from "react-toastify";
import * as Yup from "yup";
import { Container } from '@mui/material'
import { Field, Form, Formik } from 'formik'
import { BiUpArrowCircle } from "react-icons/bi";
import { askGpt } from '@/redux/service/chatgpt';

const PromptForm = () => {
    const [availablePrompt, setAvailablePrompt] = useState("")

    const initialValues = {
        prompt: ""
    }

    const validationSchema = Yup.object().shape({
        prompt: Yup.string().required("This field is required"),
    })

    const promptChatGpt = async (value) => {
        try{
            await askGpt(value.prompt)
            toast.success(`Prompt sent ${value.prompt}`);

        }catch(error){
            toast.error(`Prompt error ${error}`);


        }
    }

  return (
    <Container>
        <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={promptChatGpt}
        
        >
            {({ values, handleChange }) => (
            <Form>
                <div>
                    <div className='w-full flex items-center border border-gray rounded-lg bg-white px-4'>
                    <Field
                        className="py-4 focus:outline-none w-full"
                        type="text" 
                        name="prompt" 
                        placeholder="Message HealthGPT..." 
                        onChange={(e) => {
                            handleChange(e);
                            setAvailablePrompt(e.target.value);
                          }}
                    />
                    <button disabled={availablePrompt ? false : true } type='submit'>
                        <BiUpArrowCircle className={`text-4xl ${availablePrompt ? "bg-primary" : "bg-gray" }  rounded-lg text-white`}/>                    </button>
                    </div>
                </div>
            </Form>
            )}
        </Formik>
    </Container>
  )
}

export default PromptForm