import { IncomingHttpHeaders } from "http";
import { NextRequest, NextResponse } from "next/server";
import multiparty from "multiparty";
import { Readable } from "stream";
import fs from "fs";
import FormData from "form-data";
import fetch from "node-fetch";

export const runtime = "nodejs"; // 将 config 替换为 runtime

class IncomingMessageAdapter extends Readable {
    headers: IncomingHttpHeaders;

    constructor(request: NextRequest) {
        super();
        this.headers = Object.fromEntries(request.headers.entries());

        const reader = request.body?.getReader();
        if (reader) {
            const readStream = this;
            const process = ({
                done,
                value,
            }: ReadableStreamReadResult<Uint8Array>): void => {
                if (done) {
                    readStream.push(null);
                    return;
                }
                if (value) {
                    readStream.push(Buffer.from(value));
                    reader.read().then(process);
                }
            };
            reader.read().then(process);
        }
    }
}

export async function POST(request: NextRequest): Promise<void | Response> {
    const form = new multiparty.Form();

    type FormParseResult = {
        fields: multiparty.Fields;
        files: multiparty.Files;
    };

    try {
        const req = new IncomingMessageAdapter(request);

        const { fields, files } = await new Promise<FormParseResult>(
            (resolve, reject) => {
                form.parse(req as any, (err, fields, files) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve({ fields, files });
                    }
                });
            }
        );

        const file = files.file[0];
        const fileStream = fs.createReadStream(file.path);

        const formData = new FormData();
        formData.append("file", fileStream, file.originalFilename);
        formData.append("parse_mode", fields.parse_mode[0]);
        formData.append("langs", fields.langs[0]);
        formData.append("extract_images", fields.extract_images[0]);

        const response = await fetch("http://127.0.0.1:8765/api/v1/convert", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Error uploading file to Flask API");
        }

        const result = await response.json();

        return NextResponse.json(result);
    } catch (error) {
        return NextResponse.json({ error: "Error uploading file" });
    }
}
