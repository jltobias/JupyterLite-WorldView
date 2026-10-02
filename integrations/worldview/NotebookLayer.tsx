// Original companion adapter, MIT. Mount as a child of upstream GlobeViewer.
import { useEffect } from 'react';
import { useCesium } from 'resium';
import { Color, ColorMaterialProperty, ConstantProperty, CzmlDataSource, GeoJsonDataSource } from 'cesium';
import type { DataSource } from 'cesium';

type Props = { url: string; format: 'geojson' | 'czml'; onError?: (message: string) => void };

export default function NotebookLayer({ url, format, onError }: Props) {
  const { viewer } = useCesium();
  useEffect(() => {
    if (!viewer) return;
    let cancelled = false;
    let owned: DataSource | undefined;
    async function load() {
      try {
        // Use a reviewed local URL from public/lab; do not insert user-supplied remote URLs.
        if (!url.startsWith('/lab/') || url.includes('..') || url.includes('?') || url.includes('#')) {
          throw new Error('Use a reviewed same-origin /lab/ asset.');
        }
        const source = format === 'czml'
          ? await CzmlDataSource.load(url)
          : await GeoJsonDataSource.load(url, { clampToGround: false });
        if (cancelled || viewer!.isDestroyed()) return;
        if (format === 'geojson') {
          for (const entity of source.entities.values) {
            const height = entity.properties?.height_m?.getValue(viewer!.clock.currentTime);
            if (entity.polygon && typeof height === 'number' && Number.isFinite(height)) {
              entity.polygon.height = new ConstantProperty(0);
              entity.polygon.extrudedHeight = new ConstantProperty(Math.max(0, Math.min(100000, height)));
              entity.polygon.material = new ColorMaterialProperty(Color.CYAN.withAlpha(0.6));
            }
          }
        }
        owned = source;
        await viewer!.dataSources.add(source);
        if (cancelled && !viewer!.isDestroyed()) viewer!.dataSources.remove(source, true);
        if (!viewer!.isDestroyed()) viewer!.scene.requestRender();
      } catch (error) {
        if (!cancelled) onError?.(error instanceof Error ? error.message : String(error));
      }
    }
    void load();
    return () => {
      cancelled = true;
      if (owned && !viewer.isDestroyed()) viewer.dataSources.remove(owned, true);
    };
  }, [viewer, url, format, onError]);
  return null;
}
