import React from "react";

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
}

const isPageSelectable = (file: File | null) => {
    if (!file) return false;
    const fileExtension = file.name.split(".").pop()?.toLowerCase();
    return (
        fileExtension === "pdf" ||
        fileExtension === "doc" ||
        fileExtension === "docx"
    );
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
}) => {
    return (
        <form
            onSubmit={handleSubmit}
            className="space-y-6 w-full bg-base-100 p-6 rounded-lg shadow"
        >
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
                    <option value="auto">Auto</option>
                    <option value="general">General</option>
                    <option value="book">Book</option>
                    <option value="law">Law</option>
                    <option value="manual">Manual</option>
                    <option value="paper">Paper</option>
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
                    {/* first_page */}
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

                    {/* last_page */}
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
            <div className="form-control mt-6">
                <button type="submit" className="btn btn-primary">
                    Convert
                </button>
            </div>
        </form>
    );
};

export default FileUploadForm;
