import { useState } from "react";
import {
  Alert,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View
} from "react-native";
import { useBridge } from "@apps-in-toss/framework";

import { analyzeBirth, type BirthInfo } from "../../services/api";
import { setCachedChart } from "../../state/chart_state";

const parseNumber = (value: string, fallback: number): number => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
};

export default function HomeScreen() {
  const bridge = useBridge();
  const [year, setYear] = useState("1990");
  const [month, setMonth] = useState("6");
  const [day, setDay] = useState("24");
  const [hour, setHour] = useState("12");
  const [isLunar, setIsLunar] = useState(false);
  const [gender, setGender] = useState("M");

  const handleCalculate = async () => {
    const payload: BirthInfo = {
      year: parseNumber(year, 1990),
      month: parseNumber(month, 1),
      day: parseNumber(day, 1),
      hour: parseNumber(hour, 0),
      is_lunar: isLunar,
      gender
    };

    try {
      await bridge.ui?.showLoading?.();
      const chart = await analyzeBirth(payload);
      setCachedChart(chart);
      await bridge.ui?.hideLoading?.();
      bridge.navigation?.push?.("/chart");
    } catch (error) {
      await bridge.ui?.hideLoading?.();
      Alert.alert("Error", "Failed to calculate chart.");
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Jami Dusu Chart</Text>

      <View style={styles.field}>
        <Text style={styles.label}>Year</Text>
        <TextInput
          style={styles.input}
          keyboardType="number-pad"
          value={year}
          onChangeText={setYear}
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Month</Text>
        <TextInput
          style={styles.input}
          keyboardType="number-pad"
          value={month}
          onChangeText={setMonth}
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Day</Text>
        <TextInput
          style={styles.input}
          keyboardType="number-pad"
          value={day}
          onChangeText={setDay}
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Hour</Text>
        <TextInput
          style={styles.input}
          keyboardType="number-pad"
          value={hour}
          onChangeText={setHour}
        />
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Calendar</Text>
        <View style={styles.row}>
          <Pressable
            style={[styles.chip, !isLunar && styles.chipActive]}
            onPress={() => setIsLunar(false)}
          >
            <Text style={styles.chipText}>Solar</Text>
          </Pressable>
          <Pressable
            style={[styles.chip, isLunar && styles.chipActive]}
            onPress={() => setIsLunar(true)}
          >
            <Text style={styles.chipText}>Lunar</Text>
          </Pressable>
        </View>
      </View>

      <View style={styles.field}>
        <Text style={styles.label}>Gender</Text>
        <View style={styles.row}>
          <Pressable
            style={[styles.chip, gender === "M" && styles.chipActive]}
            onPress={() => setGender("M")}
          >
            <Text style={styles.chipText}>M</Text>
          </Pressable>
          <Pressable
            style={[styles.chip, gender === "F" && styles.chipActive]}
            onPress={() => setGender("F")}
          >
            <Text style={styles.chipText}>F</Text>
          </Pressable>
        </View>
      </View>

      <Pressable style={styles.primaryButton} onPress={handleCalculate}>
        <Text style={styles.primaryButtonText}>Generate Chart</Text>
      </Pressable>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 20,
    gap: 16
  },
  title: {
    fontSize: 24,
    fontWeight: "600"
  },
  field: {
    gap: 8
  },
  label: {
    fontSize: 14,
    fontWeight: "500"
  },
  input: {
    borderWidth: 1,
    borderColor: "#d0d0d0",
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10
  },
  row: {
    flexDirection: "row",
    gap: 8
  },
  chip: {
    borderWidth: 1,
    borderColor: "#b0b0b0",
    borderRadius: 999,
    paddingVertical: 8,
    paddingHorizontal: 16
  },
  chipActive: {
    backgroundColor: "#111",
    borderColor: "#111"
  },
  chipText: {
    color: "#111"
  },
  primaryButton: {
    marginTop: 8,
    backgroundColor: "#111",
    borderRadius: 10,
    paddingVertical: 14,
    alignItems: "center"
  },
  primaryButtonText: {
    color: "#fff",
    fontWeight: "600"
  }
});
