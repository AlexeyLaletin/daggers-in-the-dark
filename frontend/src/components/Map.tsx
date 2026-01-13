import { useState } from "react";
import { MapCanvas } from "./MapCanvas";
import { MapToolbar } from "./MapToolbar";
import { LayerControl } from "./LayerControl";
import { AddPlaceForm } from "./AddPlaceForm";
import { useMap } from "../contexts/MapContext";

export function Map(): JSX.Element {
  const { mapState, setMode } = useMap();
  const [pendingPlace, setPendingPlace] = useState<{ x: number; y: number } | null>(null);

  const handleMapClick = (x: number, y: number) => {
    if (mapState.mode === "add-poi") {
      setPendingPlace({ x, y });
    }
  };

  const handlePlaceCreated = () => {
    setPendingPlace(null);
    setMode("pan");
    // Reload places - MapCanvas will handle this via useEffect
  };

  const handleCancel = () => {
    setPendingPlace(null);
    setMode("pan");
  };

  return (
    <div
      style={{
        flex: 1,
        position: "relative",
        display: "flex",
        flexDirection: "column",
        overflow: "hidden",
      }}
    >
      <MapToolbar />
      <LayerControl />
      <MapCanvas onMapClick={handleMapClick} />

      {/* Add Place Form Modal */}
      {pendingPlace && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            zIndex: 1000,
            maxWidth: "400px",
            width: "90%",
            boxShadow: "0 4px 8px rgba(0,0,0,0.2)",
          }}
        >
          <AddPlaceForm
            position={pendingPlace}
            onSuccess={handlePlaceCreated}
            onCancel={handleCancel}
          />
        </div>
      )}

      {/* Backdrop when form is open */}
      {pendingPlace && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: "rgba(0,0,0,0.3)",
            zIndex: 999,
          }}
          onClick={handleCancel}
        />
      )}
    </div>
  );
}
