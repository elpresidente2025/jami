export type BirthInfo = {
  year: number;
  month: number;
  day: number;
  hour: number;
  is_lunar: boolean;
  is_intercalation?: boolean;
  gender: string;
};

export type Palace = {
  index: number;
  name: string;
  stars: string[];
};

export type StarPlacement = {
  star: string;
  palace_index: number;
};

export type StarMetadata = {
  star: string;
  offset: number;
  meaning: string;
  keywords: string[];
  quality: string;
};

export type PalaceMetadata = {
  index: number;
  name: string;
  theme: string;
  keywords: string[];
};

export type LunarDateInfo = {
  year: number;
  month: number;
  day: number;
  is_intercalation: boolean;
};

export type ChartResponse = {
  ming_gong: number;
  guo_shu: number;
  jami_position: number;
  jami_direction: string;
  hour_branch: number;
  hour_branch_name: string;
  palace_layout: Palace[];
  stars_data: StarPlacement[];
  stars_meta: StarMetadata[];
  palace_meta: PalaceMetadata[];
  summary: string;
  lunar_date: LunarDateInfo;
  chart_id?: number;
};

const getApiBase = (): string => {
  const globalAny = globalThis as {
    API_URL?: string;
    process?: { env?: { API_URL?: string } };
  };
  return globalAny.API_URL ?? globalAny.process?.env?.API_URL ?? "http://localhost:8000";
};

const API_BASE = getApiBase();

export const analyzeBirth = async (
  payload: BirthInfo
): Promise<ChartResponse> => {
  const response = await fetch(`${API_BASE}/api/v1/birth/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API error ${response.status}: ${message}`);
  }

  return (await response.json()) as ChartResponse;
};
