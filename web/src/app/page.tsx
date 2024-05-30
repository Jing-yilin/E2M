"use client";

import Head from "next/head";
import { useState } from "react";

export default function Home() {
    const [file, setFile] = useState<File | null>(null);
    const [parseMode, setParseMode] = useState("auto");
    const [langs, setLangs] = useState("en,zh");
    const [extractImages, setExtractImages] = useState(false);
    // result format:
    //{
    //   "message": "# 《大学生就业政策形式及应对》\n# 课程论文\n学    院：萨塞克斯人工智能学院\n\n班    级：\n\n学 　 号：\n\n学生姓名：\n\n任教老师：黎美杉\n\n二○二四 年  月\n\n大学生就业形势与政策及对策\n"
    // }

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

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
            <Head>
                <title>E2M Converter</title>
            </Head>
            <main className="bg-white rounded-lg shadow-lg p-8 w-full max-w-4xl">
                <h1 className="text-5xl font-extrabold mb-8 text-center text-gray-800">
                    E2M Converter
                </h1>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label
                            htmlFor="file"
                            className="block text-lg font-medium text-gray-700"
                        >
                            Upload file:
                        </label>
                        <input
                            type="file"
                            id="file"
                            name="file"
                            onChange={(e) =>
                                setFile(
                                    e.target.files ? e.target.files[0] : null
                                )
                            }
                            className="mt-2 p-3 w-full border border-gray-300 rounded-lg"
                            required
                        />
                    </div>
                    <div>
                        <label
                            htmlFor="parse_mode"
                            className="block text-lg font-medium text-gray-700"
                        >
                            Parse mode:
                        </label>
                        <select
                            id="parse_mode"
                            name="parse_mode"
                            value={parseMode}
                            onChange={(e) => setParseMode(e.target.value)}
                            className="mt-2 p-3 w-full border border-gray-300 rounded-lg"
                        >
                            <option value="auto">Auto</option>
                            <option value="general">General</option>
                            <option value="book">Book</option>
                            <option value="law">Law</option>
                            <option value="manual">Manual</option>
                            <option value="paper">Paper</option>
                        </select>
                    </div>
                    <div>
                        <label
                            htmlFor="langs"
                            className="block text-lg font-medium text-gray-700"
                        >
                            Languages:
                        </label>
                        <input
                            type="text"
                            id="langs"
                            name="langs"
                            value={langs}
                            onChange={(e) => setLangs(e.target.value)}
                            className="mt-2 p-3 w-full border border-gray-300 rounded-lg"
                            placeholder="en,zh"
                        />
                    </div>
                    <div>
                        <label
                            htmlFor="extract_images"
                            className="block text-lg font-medium text-gray-700"
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
                                className="h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                            />
                            <label
                                htmlFor="extract_images"
                                className="ml-2 text-gray-700"
                            >
                                Yes
                            </label>
                        </div>
                    </div>
                    <button
                        type="submit"
                        className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-700 text-white text-lg font-bold rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
                    >
                        Convert
                    </button>
                </form>
                {result && (
                    <div className="mt-8">
                        <h2 className="text-2xl font-bold mb-4">
                            Conversion Result
                        </h2>
                        <pre className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-96">
                            {result}
                        </pre>
                    </div>
                )}
            </main>
        </div>
    );
}
