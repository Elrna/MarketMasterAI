// typings.d.ts
interface Window {
    electronAPI: {
        readCSV: (callback: (data: any[]) => void) => void;
    };
}
