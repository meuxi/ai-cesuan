import { HistoryRecord } from '../types';
import { logger } from '@/utils/logger';

const STORAGE_KEY = 'liu_yao_history_v1';

export const getHistory = (): HistoryRecord[] => {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
    } catch (e) {
        logger.error("Failed to read history", e);
        return [];
    }
};

export const saveRecord = (record: HistoryRecord) => {
    try {
        const current = getHistory();
        const index = current.findIndex(r => r.id === record.id);

        let updated;
        if (index >= 0) {
            updated = [...current];
            updated[index] = record;
        } else {
            updated = [record, ...current].slice(0, 50);
        }

        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
    } catch (e) {
        logger.error("Failed to save record", e);
    }
};

export const clearHistory = () => {
    localStorage.removeItem(STORAGE_KEY);
};
