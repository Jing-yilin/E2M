"use client";

import React, { useState } from "react";
import ThemeSwitcher from "@/components/ThemeSwitcher";
import Head from "next/head";
import FileUploadForm from "@/components/FileUploadForm";
// import ConversionResult from "@/components/ConversionResult";
import Loader from "@/components/Loader";
import MarkdownPreview from "@/components/MarkdownPreview";
import JSONPreview from "@/components/JSONPreview";

export default function Home() {
    const [file, setFile] = useState<File | null>(null);
    const [parseMode, setParseMode] = useState("auto");
    const [langs, setLangs] = useState("en,zh");
    const [extractImages, setExtractImages] = useState(false);
    const [result, setResult] = useState<any | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [firstPage, setFirstPage] = useState<number | null>(null);
    const [lastPage, setLastPage] = useState<number | null>(null);
    const [use_llm, setUse_llm] = useState<boolean>(false);
    const [model_source, setModel_source] = useState<string>("gpt-3.5-turbo");
    const [model, setModel] = useState<string>("gpt-3.5-turbo");
    const [returnType, setReturnType] = useState<string>("md");
    const [enforcedJsonFormat, setEnforcedJsonFormat] = useState<string | null>(
        null
    );
    const [save_to_cache, setSave_to_cache] = useState<boolean>(false);
    const [use_cache, setUse_cache] = useState<boolean>(false);

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!file) return;

        setLoading(true); // 开始加载动画

        const formData = new FormData();
        formData.append("file", file);
        formData.append("parse_mode", parseMode);
        formData.append("langs", langs);
        formData.append("extract_images", String(extractImages));
        if (firstPage !== null)
            formData.append("first_page", String(firstPage));
        if (lastPage !== null) formData.append("last_page", String(lastPage));
        if (use_llm) formData.append("use_llm", String(use_llm));
        formData.append("model", model);
        formData.append("return_type", returnType);
        if (enforcedJsonFormat)
            formData.append("enforced_json_format", enforcedJsonFormat);
        formData.append("save_to_cache", String(save_to_cache));
        formData.append("use_cache", String(use_cache));

        try {
            const response = await fetch(
                "http://127.0.0.1:8765/api/v1/convert",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const result = await response.json();
            setResult(result);
            console.log(result);
        } catch (error) {
            console.error("Error:", error);
        } finally {
            setLoading(false); // 停止加载动画
        }
    };

    // const handleCopy = () => {
    //     if (result) {
    //         const resultString = JSON.stringify(result, null, 2);
    //         navigator.clipboard.writeText(resultString);
    //         const alert = document.createElement("div");
    //         alert.className =
    //             "fixed bottom-4 right-4 bg-blue-500 text-white p-2 rounded-lg";
    //         alert.textContent = "Result copied to clipboard!";
    //         document.body.appendChild(alert);
    //         setTimeout(() => {
    //             alert.classList.add("opacity-0");
    //             setTimeout(() => {
    //                 document.body.removeChild(alert);
    //             }, 1000);
    //         }, 1000);
    //     }
    // };

    return (
        <div className="min-h-screen flex flex-col bg-base-200 text-base-content">
            <Head>
                <title>E2M Converter</title>
            </Head>
            <header className="w-full bg-base-100 shadow">
                <nav className="navbar max-w-7xl mx-auto">
                    <div className="flex-1">
                        <a className="btn btn-ghost normal-case text-xl">E2M</a>
                    </div>
                    <div className="flex-none">
                        <a
                            href="http://127.0.0.1:8765/swagger/"
                            className="btn btn-ghost"
                        >
                            Documentation
                        </a>
                        <ThemeSwitcher />
                    </div>
                </nav>
            </header>
            <main className="flex flex-col items-center justify-center flex-1 w-full max-w-6xl p-8 mx-auto">
                <h1 className="text-5xl font-extrabold mb-8 text-center">
                    E2M Converter
                </h1>
                <p className="mb-4 text-center text-sm">
                    📂Supported file types: [doc, docx, ppt, pptx, pdf, html, htm]
                </p>
                <p className="mb-4 text-center text-sm">
                    💡Tip: It may take a few minutes to download the model for
                    the first time converting pdf.
                </p>
                <FileUploadForm
                    file={file}
                    setFile={setFile}
                    parseMode={parseMode}
                    setParseMode={setParseMode}
                    langs={langs}
                    setLangs={setLangs}
                    extractImages={extractImages}
                    setExtractImages={setExtractImages}
                    firstPage={firstPage}
                    setFirstPage={setFirstPage}
                    lastPage={lastPage}
                    setLastPage={setLastPage}
                    handleSubmit={handleSubmit}
                    use_llm={use_llm}
                    setUse_llm={setUse_llm}
                    model_source={model_source}
                    setModel_source={setModel_source}
                    model={model}
                    setModel={setModel}
                    returnType={returnType}
                    setReturnType={setReturnType}
                    enforcedJsonFormat={enforcedJsonFormat}
                    setEnforcedJsonFormat={setEnforcedJsonFormat}
                    save_to_cache={save_to_cache}
                    setSave_to_cache={setSave_to_cache}
                    use_cache={use_cache}
                    setUse_cache={setUse_cache}
                />
                {loading && <Loader />}
                {result && (
                    <>
                        {/* <ConversionResult
                            result={JSON.stringify(result, null, 2)}
                            handleCopy={handleCopy}
                        /> */}
                        {result.md_data && (
                            <MarkdownPreview
                                markdownContent={result.md_data.content}
                            />
                        )}
                        {<JSONPreview jsonContent={result} />}
                    </>
                )}
            </main>
        </div>
    );
}
