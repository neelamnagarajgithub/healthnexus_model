const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const app = express();
const port = 8099;

app.use(bodyParser.json());

app.post('/predict', (req, res) => {const patientData = JSON.stringify(req.body);

    const pythonProcess = spawn('python', ['predictor-model.py']);

    pythonProcess.stdin.write(patientData);
    pythonProcess.stdin.end();

    let result = '';
    pythonProcess.stdout.on('data', (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send('Internal Server Error');
        }
        res.send({ specialty: result.trim() });
    });
});
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});