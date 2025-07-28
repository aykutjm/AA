const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer();

app.post('/decrypt', upload.single('data'), (req, res) => {
  const fileBuffer = req.file.buffer;

  // Şifre çözme işlemi
  res.send('POST geldi ✅');
});

app.listen(3000, () => console.log('Server running...'));
