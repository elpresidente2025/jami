export type BirthInfo = {
  year: number;
  month: number;
  day: number;
  hour: number;
  is_lunar: boolean;
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

export type ChartResponse = {
  ming_gong: number;
  guo_shu: number;
  jami_position: number;
  palace_layout: Palace[];
  stars_data: StarPlacement[];
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
