import { createContext } from 'react';
import { Viewer as CesiumViewer } from 'cesium';
import { CesiumComponentRef } from 'resium';

export const CesiumContext = createContext<{
    viewerRef: CesiumComponentRef<CesiumViewer> | null
    connected: boolean
}>({
    viewerRef: null,
    connected: false,
});