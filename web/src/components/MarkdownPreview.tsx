import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

interface MarkdownPreviewProps {
    markdownContent: string;
}

const MarkdownPreview: React.FC<MarkdownPreviewProps> = ({ markdownContent }) => {
    return (
        <div className="markdown-preview bg-base-100 p-6 rounded-lg shadow max-w-full w-full mt-4">
            <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                className="prose"
            >
                {markdownContent}
            </ReactMarkdown>
        </div>
    );
};

export default MarkdownPreview;
