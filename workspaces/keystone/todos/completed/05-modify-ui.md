# Task #9 — Modify (Inline Edit) Frontend

> Status: pending | Priority: CRITICAL | Depends on: none

---

## What

SuggestionCard component has Accept and Skip buttons but no Modify option. Add inline edit capability: user can click Modify to expand the card, edit the suggested rewrite, and submit the modified version.

---

## Deliverables

### 1. Update SuggestionCard to include Modify button

**File**: `apps/web/src/components/keystone/SuggestionCard.tsx` (or wherever SuggestionCard lives)

Add state:

```typescript
const [isEditing, setIsEditing] = useState(false);
const [modifiedText, setModifiedText] = useState(suggestion.suggested_text);
```

Add Modify button alongside Accept/Skip:

```typescript
<div className="suggestion-actions">
  <button onClick={() => setIsEditing(true)}>Modify</button>
  <button onClick={handleAccept}>Accept</button>
  <button onClick={handleSkip}>Skip</button>
</div>
```

Add inline edit view (shown when isEditing=true):

```typescript
{isEditing && (
  <div className="suggestion-edit">
    <label>Edit your version:</label>
    <textarea
      value={modifiedText}
      onChange={(e) => setModifiedText(e.target.value)}
      rows={4}
    />
    <div className="edit-actions">
      <button onClick={handleSubmitModify}>Submit</button>
      <button onClick={() => setIsEditing(false)}>Cancel</button>
    </div>
  </div>
)}
```

### 2. Handle submitModify API call

```typescript
const handleSubmitModify = async () => {
  await fetch(`/api/suggestions/${suggestion.id}/modify`, {
    method: "POST",
    body: JSON.stringify({ modified_text: modifiedText }),
  });
  // Update signal to MODIFIED
  await fetch(`/api/signals`, {
    method: "POST",
    body: JSON.stringify({ suggestion_id: suggestion.id, action: "MODIFIED" }),
  });
  setIsEditing(false);
  onUpdate(suggestion.id, "MODIFIED");
};
```

### 3. Ensure backend modify endpoint exists

**File**: `src/keystone/api/suggestions.py`

Already exists per audit, but verify:

```python
@router.post("/suggestions/{suggestion_id}/modify")
async def modify_suggestion(
    suggestion_id: int,
    modified_text: str,
    current_user: User = Depends(get_current_user),
):
    suggestion = await db.suggestions.get(suggestion_id)
    if suggestion.user_id != current_user.id:
        raise HTTPException(403)

    suggestion.modified_text = modified_text
    suggestion.original_text = suggestion.original_text  # Preserve original
    await db.suggestions.save(suggestion)

    # Log signal
    await db.signals.create(
        suggestion_id=suggestion_id,
        action="MODIFIED",
        user_id=current_user.id,  # For signal logging (anonymized for training)
    )

    return {"status": "ok"}
```

---

## Acceptance Criteria

- [ ] SuggestionCard shows Modify button
- [ ] Clicking Modify expands inline edit area with textarea
- [ ] Original suggestion text is pre-filled in textarea
- [ ] Submit calls POST /api/suggestions/{id}/modify with modified_text
- [ ] Signal is logged as MODIFIED
- [ ] Cancel collapses the edit view without calling API
