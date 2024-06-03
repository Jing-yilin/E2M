import React from "react";

interface ConversionResultProps {
    result: string;
    handleCopy: () => void;
}

const ConversionResult: React.FC<ConversionResultProps> = ({
    result,
    handleCopy,
}) => {
    return (
        <div className="relative w-full bg-base-100 p-6 rounded-lg shadow max-w-full w-full mt-4">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Conversion Result</h2>
                <button
                    onClick={handleCopy}
                    className="btn btn-outline btn-primary"
                >
                    Copy
                </button>
            </div>
            <pre className=" p-4 rounded-lg overflow-auto max-h-96 text-sm">
                {result}
            </pre>
        </div>
    );
};

export default ConversionResult;
