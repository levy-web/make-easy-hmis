import OpenAI from 'openai';

export default async function handler(req, res) {
    try {
        const { params } = req.body;

        if (!params || !params.prompt) {
            return res.status(400).json({ error: "Prompt is required in the request body" });
        }

        console.log("PROMPT FROM GPT API", params.prompt);

        // const openai = new OpenAI({
        //     apiKey: process.env['NEXT_PUBLIC_OPENAI_API_KEY'],
        //     // Add other configuration options as needed
        // });

        const openai = new OpenAI({
            apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY // This is also the default, can be omitted
        });

        const result = await openai.completions.create({
            model: "gpt-3.5-turbo-instruct",
            prompt: "This story begins",
            max_tokens: 30,
          });

        return res.json({ answer: result.choices[0].text });

    } catch (error) {
        console.error("Error:", error);
        return res.status(500).json({ error: "Error fetching answer from the GPT API" });
    }
}
