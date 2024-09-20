const { AutoTokenizer, AutoModelForCausalLM } = require('@huggingface/inference');
console.log(AutoTokenizer, AutoModelForCausalLM); // Check if they are defined
const { AutoDistributedModelForCausalLM } = require('petals');

async function main() {
  // Load the tokenizer and model
  const modelName = 'petals-team/StableBeluga2'; // Replace with your desired model
  const tokenizer = await AutoTokenizer.from_pretrained(modelName);
  const model = await AutoModelForCausalLM.from_pretrained(modelName);

  // Connect to the Petals swarm
  await model.connect();

  // Generate text
  const inputText = 'A cat in French is "';
  const inputs = tokenizer.encode(inputText, { return_tensors: 'pt' });
  const outputs = await model.generate(inputs, { max_new_tokens: 3 });
  const generatedText = tokenizer.decode(outputs[0]);
  console.log(generatedText); // Output: A cat in French is "chat" and

  // Run inference session for interactive chat
  const fakeToken = tokenizer.encode('^')[0]; // Workaround for tokenizer.decode()
  const maxSessionLength = 30;
  const session = await model.inference_session({ max_length: maxSessionLength });

  while (true) {
    const prompt = await new Promise(resolve => {
      process.stdin.once('data', data => resolve(data.toString().trim()));
    });

    if (prompt === '') {
      break;
    }

    const prefix = `Human: ${prompt}\nFriendly AI:`;
    const prefixTokens = tokenizer.encode(prefix, { return_tensors: 'pt' });
    console.log('Friendly AI:'); // Corrected line

    let response = '';
    let currentTokens = prefixTokens;

    while (true) {
      const outputs = await model.generate(currentTokens, {
        max_new_tokens: 1,
        session,
        do_sample: true,
        temperature: 0.9,
        top_p: 0.6,
      });

      const newToken = outputs[0, -1].item();
      const decodedToken = tokenizer.decode([fakeToken, newToken]);
      response += decodedToken;
      console.log(decodedToken); // Corrected line

      currentTokens = newToken.reshape(1, 1);

      if (response.includes('\n') || response.includes('</s>')) {
        break;
      }
    }
  }

  // Close the inference session
  await session.close();

  // Disconnect from the Petals swarm
  await model.disconnect();
}

main().catch(error => {
  console.error('Error:', error);
});