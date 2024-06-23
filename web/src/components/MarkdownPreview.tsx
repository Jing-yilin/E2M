import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeToc from "rehype-toc";

interface MarkdownPreviewProps {
    markdownContent: string;
}

const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({
    markdownContent,
}) => {
    const downloadMarkdown = () => {
        const blob = new Blob([markdownContent], { type: "text/markdown" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        const timestamp = new Date().toLocaleString("zh-CN", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
        });
        a.href = url;
        a.download = `markdown-${timestamp}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const copyToClipboard = () => {
        navigator.clipboard
            .writeText(markdownContent)
            .then(() => {
                alert("Markdown content copied to clipboard!");
            })
            .catch((err) => {
                console.error("Failed to copy: ", err);
            });
    };

    return (
        <div className="relative bg-base-100 p-6 rounded-lg shadow max-w-full w-full mt-4">
            <div className="absolute top-2 right-2 flex space-x-2">
                <button
                    onClick={downloadMarkdown}
                    className="p-2 bg-base-200 text-base-content rounded"
                >
                    Download
                </button>
                <button
                    onClick={copyToClipboard}
                    className="p-2 bg-base-200 text-base-content rounded"
                >
                    Copy
                </button>
            </div>
            <ReactMarkdown
                remarkPlugins={[remarkGfm, rehypeToc]}
                rehypePlugins={[rehypeRaw]}
                className="prose dark:prose-dark"
            >
                {markdownContent}
            </ReactMarkdown>
        </div>
    );
};

export default MarkdownPreview;
