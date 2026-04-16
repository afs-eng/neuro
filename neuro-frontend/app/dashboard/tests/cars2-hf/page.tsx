import { Suspense } from "react";

import CARS2HFPage from "./page.client";

export default function Page() {
  return (
    <Suspense fallback={<div className="py-16 text-center text-slate-500">Carregando CARS2-HF...</div>}>
      <CARS2HFPage />
    </Suspense>
  );
}
