"use client";

import React, { useState } from "react";
import ThemeSwitcher from "../components/ThemeSwitcher";
import Head from "next/head";

export default function Home() {
    const [file, setFile] = useState<File | null>(null);
    const [parseMode, setParseMode] = useState("auto");
    const [langs, setLangs] = useState("en,zh");
    const [extractImages, setExtractImages] = useState(false);
    const [result, setResult] = useState<string | null>(null);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);
        formData.append("parse_mode", parseMode);
        formData.append("langs", langs);
        formData.append("extract_images", String(extractImages));

        const response = await fetch("http://127.0.0.1:8765/api/v1/convert", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        setResult(result.message);
        console.log(result);
    };

    const handleCopy = () => {
        if (result) {
            navigator.clipboard.writeText(result);
            const alert = document.createElement("div");
            alert.className =
                "fixed bottom-4 right-4 bg-blue-500 text-white p-2 rounded-lg";
            alert.textContent = "Result copied to clipboard!";
            document.body.appendChild(alert);
            setTimeout(() => {
                alert.classList.add("opacity-0");
                setTimeout(() => {
                    document.body.removeChild(alert);
                }, 1000);
            }, 1000);
        }
    };

    return (
        <div className="h-screen flex flex-col items-center justify-center bg-base-200 text-base-content relative">
            <Head>
                <title>E2M Converter</title>
            </Head>
            <ThemeSwitcher />
            <main className="card w-full max-w-4xl shadow-lg bg-base-100">
                <div className="card-body">
                    <h1 className="card-title text-5xl font-extrabold mb-8 text-center">
                        E2M Converter
                    </h1>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="form-control">
                            <label
                                htmlFor="file"
                                className="label text-lg font-medium text-center"
                            >
                                Upload file:
                            </label>
                            <input
                                type="file"
                                id="file"
                                name="file"
                                onChange={(e) =>
                                    setFile(
                                        e.target.files
                                            ? e.target.files[0]
                                            : null
                                    )
                                }
                                className="file-input file-input-bordered file-input-primary w-full"
                                required
                            />
                        </div>

                        <div className="form-control">
                            <label
                                htmlFor="parse_mode"
                                className="label text-lg font-medium"
                            >
                                Parse mode:
                            </label>
                            <select
                                id="parse_mode"
                                name="parse_mode"
                                value={parseMode}
                                onChange={(e) => setParseMode(e.target.value)}
                                className="select select-bordered"
                            >
                                <option value="auto">Auto</option>
                                <option value="general">General</option>
                                <option value="book">Book</option>
                                <option value="law">Law</option>
                                <option value="manual">Manual</option>
                                <option value="paper">Paper</option>
                            </select>
                        </div>
                        <div className="form-control">
                            <label
                                htmlFor="langs"
                                className="label text-lg font-medium"
                            >
                                Languages:
                            </label>
                            <input
                                type="text"
                                id="langs"
                                name="langs"
                                value={langs}
                                onChange={(e) => setLangs(e.target.value)}
                                className="input input-bordered"
                                placeholder="en,zh"
                            />
                        </div>
                        <div className="form-control">
                            <label
                                htmlFor="extract_images"
                                className="label text-lg font-medium"
                            >
                                Extract images:
                            </label>
                            <div className="flex items-center mt-2">
                                <input
                                    type="checkbox"
                                    id="extract_images"
                                    name="extract_images"
                                    checked={extractImages}
                                    onChange={(e) =>
                                        setExtractImages(e.target.checked)
                                    }
                                    className="checkbox checkbox-primary"
                                />
                                <label
                                    htmlFor="extract_images"
                                    className="ml-2"
                                >
                                    Yes
                                </label>
                            </div>
                        </div>
                        <button
                            type="submit"
                            className="btn btn-primary w-full"
                        >
                            Convert
                        </button>
                    </form>
                    {result && (
                        <div className="mt-8 relative">
                            <h2 className="text-2xl font-bold mb-4">
                                Conversion Result
                            </h2>
                            <button
                                onClick={handleCopy}
                                className="absolute top-0 right-0 mt-0.5 mr-0.5 btn btn-outline btn-primary"
                            >
                                Copy
                            </button>
                            <pre className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96">
                                {result}
                            </pre>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
