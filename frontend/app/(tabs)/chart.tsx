import { ScrollView, StyleSheet, Text, View } from "react-native";

import { getCachedChart } from "../../state/chart_state";

export default function ChartScreen() {
  const chart = getCachedChart();

  if (!chart) {
    return (
      <View style={styles.center}>
        <Text>No chart loaded.</Text>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Chart Summary</Text>
      <View style={styles.summaryRow}>
        <Text>Ming Gong</Text>
        <Text>{chart.ming_gong}</Text>
      </View>
      <View style={styles.summaryRow}>
        <Text>Guo Shu</Text>
        <Text>{chart.guo_shu}</Text>
      </View>
      <View style={styles.summaryRow}>
        <Text>Jami Position</Text>
        <Text>{chart.jami_position}</Text>
      </View>

      <Text style={styles.sectionTitle}>Palaces</Text>
      {chart.palace_layout.map((palace) => (
        <View key={palace.index} style={styles.palaceCard}>
          <Text style={styles.palaceTitle}>
            {palace.index}. {palace.name}
          </Text>
          <Text style={styles.palaceStars}>
            {palace.stars.length ? palace.stars.join(", ") : "None"}
          </Text>
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center"
  },
  container: {
    padding: 20,
    gap: 12
  },
  title: {
    fontSize: 22,
    fontWeight: "600"
  },
  summaryRow: {
    flexDirection: "row",
    justifyContent: "space-between"
  },
  sectionTitle: {
    marginTop: 12,
    fontSize: 18,
    fontWeight: "600"
  },
  palaceCard: {
    borderWidth: 1,
    borderColor: "#e2e2e2",
    borderRadius: 10,
    padding: 12
  },
  palaceTitle: {
    fontWeight: "600"
  },
  palaceStars: {
    color: "#555",
    marginTop: 4
  }
});
