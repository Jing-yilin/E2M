declare module "multiparty" {
    import { IncomingMessage } from "http";

    interface File {
        fieldName: string;
        originalFilename: string;
        path: string;
        headers: Record<string, string>;
        size: number;
    }

    interface Fields {
        [key: string]: string[];
    }

    interface Files {
        [key: string]: File[];
    }

    type FormCallback = (
        error: Error | null,
        fields: Fields,
        files: Files
    ) => void;

    export class Form {
        parse(req: IncomingMessage, callback: FormCallback): void;
    }
}
