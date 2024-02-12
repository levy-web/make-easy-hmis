import { APP_API_URL } from "@/assets/api-endpoints";
import axios from "axios";

export const askGpt = (prompt) => {

    return new Promise((resolve,reject) =>{
        axios.post(`${APP_API_URL.CHATGPT_PROMPT}`,{
            params: {
                prompt: prompt
            }
        })
        .then((res) =>{
            resolve(res.data)
        })
        .catch((err) =>{
            reject(err.message)
        })
    })
}
