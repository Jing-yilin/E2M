import React, { useEffect, useState } from "react";
import { JSONTree } from "react-json-tree";

interface JSONPreviewProps {
    jsonContent: object;
}

const lightTheme = {
    scheme: "daisyui-light",
    base00: "#ffffff",
    base01: "#f3f4f6",
    base02: "#e5e7eb",
    base03: "#d1d5db",
    base04: "#9ca3af",
    base05: "#6b7280",
    base06: "#4b5563",
    base07: "#374151",
    base08: "#ef4444",
    base09: "#f97316",
    base0A: "#f59e0b",
    base0B: "#10b981",
    base0C: "#06b6d4",
    base0D: "#3b82f6",
    base0E: "#8b5cf6",
    base0F: "#ec4899",
};

const darkTheme = {
    scheme: "daisyui-dark",
    base00: "#111827",
    base01: "#1f2937",
    base02: "#374151",
    base03: "#4b5563",
    base04: "#6b7280",
    base05: "#9ca3af",
    base06: "#d1d5db",
    base07: "#e5e7eb",
    base08: "#ef4444",
    base09: "#f97316",
    base0A: "#f59e0b",
    base0B: "#10b981",
    base0C: "#06b6d4",
    base0D: "#3b82f6",
    base0E: "#8b5cf6",
    base0F: "#ec4899",
};

const JSONPreview: React.FC<JSONPreviewProps> = ({ jsonContent }) => {
    const [currentTheme, setCurrentTheme] = useState(lightTheme);

    useEffect(() => {
        const theme = document.documentElement.getAttribute("data-theme");
        setCurrentTheme(theme === "dark" ? darkTheme : lightTheme);
    }, []);

    return (
        <div className="json-preview bg-base-100 p-6 rounded-lg shadow max-w-full w-full mt-4">
            <JSONTree
                data={jsonContent}
                theme={currentTheme}
                invertTheme={false}
                hideRoot={true}
            />
        </div>
    );
};

export default JSONPreview;
