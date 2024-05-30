import { NextRequest, NextResponse } from 'next/server';
import multiparty from 'multiparty';
import { Readable } from 'stream';
import fs from 'fs';
import FormData from 'form-data';
import fetch from 'node-fetch';

export const config = {
  api: {
    bodyParser: false, // Ensure the body is not parsed by Next.js
  },
};

export async function POST(request: NextRequest) {
  const form = new multiparty.Form();

  return new Promise((resolve, reject) => {
    // Convert the Web Streams request to a Node.js readable stream
    const req = new Readable({
      read() {
        // Convert Web Streams request body to Buffer
        request.body?.getReader().read().then(({ value }) => {
          this.push(value);
          this.push(null);
        });
      },
    });

    req.headers = request.headers as any;

    form.parse(req, async (err, fields, files) => {
      if (err) {
        reject(new Error('Error parsing the form'));
        return;
      }

      const file = files.file[0];
      const fileStream = fs.createReadStream(file.path);

      const formData = new FormData();
      formData.append('file', fileStream, file.originalFilename);
      formData.append('parse_mode', fields.parse_mode[0]);
      formData.append('langs', fields.langs[0]);
      formData.append('extract_images', fields.extract_images[0]);

      try {
        const response = await fetch('http://127.0.0.1:8765/api/v1/convert', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();

        resolve(NextResponse.json(result));
      } catch (error) {
        reject(new Error('Error uploading file to Flask API'));
      }
    });
  });
}
