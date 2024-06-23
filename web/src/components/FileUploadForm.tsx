import React, { useEffect, useState } from "react";
import yaml from "js-yaml";

interface FileUploadFormProps {
    file: File | null;
    setFile: React.Dispatch<React.SetStateAction<File | null>>;
    parseMode: string;
    setParseMode: React.Dispatch<React.SetStateAction<string>>;
    langs: string;
    setLangs: React.Dispatch<React.SetStateAction<string>>;
    extractImages: boolean;
    setExtractImages: React.Dispatch<React.SetStateAction<boolean>>;
    firstPage: number | null;
    setFirstPage: React.Dispatch<React.SetStateAction<number | null>>;
    lastPage: number | null;
    setLastPage: React.Dispatch<React.SetStateAction<number | null>>;
    handleSubmit: (event: React.FormEvent) => void;
    use_llm: boolean;
    setUse_llm: React.Dispatch<React.SetStateAction<boolean>>;
    model_source: string;
    setModel_source: React.Dispatch<React.SetStateAction<string>>;
    model: string;
    setModel: React.Dispatch<React.SetStateAction<string>>;
    returnType: string;
    setReturnType: React.Dispatch<React.SetStateAction<string>>;
    enforcedJsonFormat: string | null;
    setEnforcedJsonFormat: React.Dispatch<React.SetStateAction<string | null>>;
    save_to_cache: boolean;
    setSave_to_cache: React.Dispatch<React.SetStateAction<boolean>>;
    use_cache: boolean;
    setUse_cache: React.Dispatch<React.SetStateAction<boolean>>;
}

const isPageSelectable = (file: File | null) => {
    if (!file) return false;
    const fileExtension = file.name.split(".").pop()?.toLowerCase();
    return fileExtension === "pdf";
};

const FileUploadForm: React.FC<FileUploadFormProps> = ({
    file,
    setFile,
    parseMode,
    setParseMode,
    langs,
    setLangs,
    extractImages,
    setExtractImages,
    firstPage,
    setFirstPage,
    lastPage,
    setLastPage,
    handleSubmit,
    use_llm,
    setUse_llm,
    model_source,
    setModel_source,
    model,
    setModel,
    returnType,
    setReturnType,
    enforcedJsonFormat,
    setEnforcedJsonFormat,
    save_to_cache,
    setSave_to_cache,
    use_cache,
    setUse_cache,
}) => {
    const [modelSources, setModelSources] = useState<{
        [key: string]: string[];
    }>({});

    useEffect(() => {
        const loadModelSources = async () => {
            try {
                const response = await fetch("/models.yaml");
                const text = await response.text();
                const data = yaml.load(text) as { [key: string]: string[] };
                setModelSources(data);
            } catch (e) {
                console.error(e);
            }
        };

        loadModelSources();
    }, []);

    useEffect(() => {
        if (model_source && modelSources[model_source]) {
            setModel(modelSources[model_source][0]);
        }
    }, [model_source, modelSources, setModel]);

    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-6 w-full bg-base-100 p-6 rounded-lg shadow"
        >
            {/* Save to cache and use cache buttons */}
            <div className="form-control">
                <label
                    htmlFor="save_to_cache"
                    className="label text-lg font-medium"
                >
                    Save to cache:
                </label>
                <div className="flex items-center mt-2">
                    <input
                        type="checkbox"
                        id="save_to_cache"
                        name="save_to_cache"
                        checked={save_to_cache}
                        onChange={(e) => setSave_to_cache(e.target.checked)}
                        className="checkbox checkbox-primary"
                    />
                    <label htmlFor="save_to_cache" className="ml-2">
                        Yes
                    </label>
                </div>
            </div>
            <div className="form-control">
                <label
                    htmlFor="use_cache"
                    className="label text-lg font-medium"
                >
                    Use cache:
                </label>
                <div className="flex items-center mt-2">
                    <input
                        type="checkbox"
                        id="use_cache"
                        name="use_cache"
                        checked={use_cache}
                        onChange={(e) => setUse_cache(e.target.checked)}
                        className="checkbox checkbox-primary"
                    />
                    <label htmlFor="use_cache" className="ml-2">
                        Yes
                    </label>
                </div>
            </div>

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
                        setFile(e.target.files ? e.target.files[0] : null)
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
                    <option value="auto">Auto(✨Recommended)</option>
                    <option value="ocr-low">OCR Low</option>
                    <option value="ocr-high">OCR High(🤖High GPU usage)</option>
                    <option value="fast">Fast</option>
                </select>
            </div>
            <div className="form-control">
                <label htmlFor="langs" className="label text-lg font-medium">
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
            {/* Extract images */}
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
                        onChange={(e) => setExtractImages(e.target.checked)}
                        className="checkbox checkbox-primary"
                    />
                    <label htmlFor="extract_images" className="ml-2">
                        Yes
                    </label>
                </div>
            </div>
            {isPageSelectable(file) && (
                <>
                    {/* First page */}
                    <div className="form-control">
                        <label
                            htmlFor="first_page"
                            className="label text-lg font-medium"
                        >
                            First page:
                        </label>
                        <input
                            type="number"
                            id="first_page"
                            name="first_page"
                            value={firstPage ?? ""}
                            onChange={(e) =>
                                setFirstPage(
                                    e.target.value
                                        ? parseInt(e.target.value)
                                        : null
                                )
                            }
                            className="input input-bordered"
                            placeholder="1"
                        />
                    </div>

                    {/* Last page */}
                    <div className="form-control">
                        <label
                            htmlFor="last_page"
                            className="label text-lg font-medium"
                        >
                            Last page:
                        </label>
                        <input
                            type="number"
                            id="last_page"
                            name="last_page"
                            value={lastPage ?? ""}
                            onChange={(e) =>
                                setLastPage(
                                    e.target.value
                                        ? parseInt(e.target.value)
                                        : null
                                )
                            }
                            className="input input-bordered"
                            placeholder="End of document"
                        />
                    </div>
                </>
            )}
            {/* Use LLM */}
            <div className="form-control">
                <label htmlFor="use_llm" className="label text-lg font-medium">
                    Use LLM (✨Recommended for clearer results):
                </label>
                <div className="flex items-center mt-2">
                    <input
                        type="checkbox"
                        id="use_llm"
                        name="use_llm"
                        checked={use_llm}
                        onChange={(e) => setUse_llm(e.target.checked)}
                        className="checkbox checkbox-primary"
                    />
                    <label htmlFor="use_llm" className="ml-2">
                        Yes
                    </label>
                </div>
            </div>
            {use_llm && (
                <>
                    {/* Model source */}
                    <div className="form-control">
                        <label
                            htmlFor="model_source"
                            className="label text-lg font-medium"
                        >
                            Model source:
                        </label>
                        <select
                            id="model_source"
                            name="model_source"
                            value={model_source}
                            onChange={(e) => setModel_source(e.target.value)}
                            className="select select-bordered"
                        >
                            {Object.keys(modelSources).map((source) => (
                                <option key={source} value={source}>
                                    {source}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Model */}
                    <div className="form-control">
                        <label
                            htmlFor="model"
                            className="label text-lg font-medium"
                        >
                            Model:
                        </label>
                        <select
                            id="model"
                            name="model"
                            value={model}
                            onChange={(e) => setModel(e.target.value)}
                            className="select select-bordered"
                        >
                            {modelSources[model_source] &&
                                modelSources[model_source].map(
                                    (modelOption) => (
                                        <option
                                            key={modelOption}
                                            value={modelOption}
                                        >
                                            {modelOption}
                                        </option>
                                    )
                                )}
                        </select>
                    </div>

                    {/* Return type */}
                    <div className="form-control">
                        <label
                            htmlFor="return_type"
                            className="label text-lg font-medium"
                        >
                            Return type:
                        </label>
                        <select
                            id="return_type"
                            name="return_type"
                            value={returnType}
                            onChange={(e) => setReturnType(e.target.value)}
                            className="select select-bordered"
                        >
                            <option value="md">Markdown</option>
                            <option value="json">JSON</option>
                        </select>
                    </div>
                    {/* Enforced JSON format */}
                    <div className="form-control">
                        <label
                            htmlFor="enforced_json_format"
                            className="label text-lg font-medium"
                        >
                            Enforced JSON format:
                        </label>
                        <input
                            type="text"
                            id="enforced_json_format"
                            name="enforced_json_format"
                            value={enforcedJsonFormat ?? ""}
                            onChange={(e) =>
                                setEnforcedJsonFormat(
                                    e.target.value ? e.target.value : null
                                )
                            }
                            className="input input-bordered"
                            placeholder="null"
                        />
                    </div>
                </>
            )}

            <div className="form-control mt-6">
                <button type="submit" className="btn btn-primary">
                    Convert
                </button>
            </div>
        </form>
    );
};

export default FileUploadForm;
