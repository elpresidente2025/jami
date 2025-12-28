import type { ChartResponse } from "../services/api";

let cachedChart: ChartResponse | null = null;

export const setCachedChart = (chart: ChartResponse): void => {
  cachedChart = chart;
};

export const getCachedChart = (): ChartResponse | null => cachedChart;

export const clearCachedChart = (): void => {
  cachedChart = null;
};
