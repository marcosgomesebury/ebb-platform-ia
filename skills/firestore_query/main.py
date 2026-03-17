from google.cloud import firestore
import time

# Substitua pelo seu partner_id real
partner_id = "SEU_PARTNER_ID"

db = firestore.Client(project="ebb-ebury-connect-dev")
collection = db.collection("hedges").document(partner_id).collection("hedges")

query = (collection
         .where("status", "==", "PENDING_LINK")
         .where("createdAt", ">=", "2026-03-10T00:00:00Z")
         .where("createdAt", "<=", "2026-03-10T23:59:59Z")
         # .where("category", "==", "GOODS")  # se necessário
         # .where("isLinked", "==", False)    # se necessário
        )

start = time.time()
results = list(query.stream())
print(f"Total: {len(results)} - Tempo: {time.time() - start:.2f}s")
