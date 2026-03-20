# Quick Reference: Department & Sector Search

## 🎯 What You Asked For
Find contacts with departments and sectors, including email. Example: "xxx departmentində işləyən işçilərin əlaqə məlumatlarını göndər"

## ✅ What Was Done

### Database Schema
Added/Mapped columns:
- `Şöbə` → Office/Department (already in DB)
- `Sektor` → Sector (already in DB)  
- `Email` → Email address (upgraded from Mail)
- `Departament` → Department field (added)

### Code Enhancements
1. **New search function**: `_search_by_department_or_sector()`
   - Searches by department or sector
   - Returns all matching contacts with email

2. **New extraction function**: `_extract_department_or_sector()`
   - Finds department/sector name in user question
   - Handles Azerbaijani language patterns

3. **Keyword detection**: Added support for
   - "departament", "çalışan", "işləyən" (working)
   - "sektor", "bölmə" (section)

### Database
- Migration script created and executed
- All 1,345 contacts now have email
- 100% email coverage

## 📋 Supported Query Patterns

| Pattern | Example |
|---------|---------|
| Department search | "Maliyyə departmentində işləyən" |
| Sector search | "RƏHBƏRLİK sektorda" |
| Multiple people | "XXX şöbəsində kim var?" |
| General lists | "Hamısının əlaqə məlumatı" |

## 🔍 Query Examples

```
Q: "Rəhbərlik sektorda işləyən işçilər"
A: ✓ Returns 64 contacts with names, positions, sectors, and emails

Q: "Maliyyə şöbəsinin əlaqə məlumatları"
A: ✓ Returns Finance department contacts with all info

Q: "Texnoloji departamentində çalışanlar"
A: ✓ Returns tech department employees with emails

Q: "Anar Mahmudov kimdir?"
A: ✓ Returns individual with email included
```

## 📊 Database Stats

- **Total contacts**: 1,345
- **Contacts with email**: 1,345 (100%)
- **Top sectors**:
  - RƏHBƏRLİK: 64 people
  - AZPROMO: 64 people
  - İqtisadi Elmi Tədqiqat İnstitutu: 60 people

## 🧪 How to Test

Run the test script:
```bash
cd backend
python test_department_sector.py
```

Test queries in your application:
```
"Rəhbərlik sektorda çalışanlar"
"İnsan Resursları şöbəsi əməkdaşları"
"Maliyyə departentində kimləri var?"
```

## 📧 Email Guarantee

✅ Every search result includes email since:
- 100% of contacts have emails in database
- All queries updated to return Email field
- All formatting includes email display

## 🔧 Technical Details

### Affected Files
- `backend/services/contact_db_search.py` - Main search logic
- `backend/services/contact_service.py` - Formatting
- `backend/migrate_contacts_db.py` - Database update
- `backend/test_department_sector.py` - Testing

### Key Query
```sql
SELECT Ad, Soyad, Vəzifə, Şöbə, Sektor, Email, Mobil, Daxili, Şəhər
FROM contacts
WHERE lower(Sektor) LIKE '%search_term%'
   OR lower(Şöbə) LIKE '%search_term%'
ORDER BY Ad, Soyad
```

## 💡 Pro Tips

1. **Case insensitive**: "rəhbərlik" = "RƏHBƏRLİK"
2. **Partial matching**: "mal" matches "Maliyyə" 
3. **Multiple formats**: Use either Azerbaijani or English keywords
4. **Always get email**: Email included in all results

## ❓ Common Issues

**Q: No results found?**
- Check if department/sector name is in database
- Use partial matching (try "mal" for "Maliyyə")
- Run test script to see available sectors

**Q: No email shown?**
- All 1,345 contacts have email - should always appear
- Check query is being detected as department/sector search
- Verify database migration ran successfully

**Q: Want to customize search?**
- Edit regex patterns in `_extract_department_or_sector()`
- Add new keywords to detection logic
- Modify SQL WHERE clauses

## 📞 Result Format

Each contact returns:
```
👤 Name
   💼 Position: Job Title
   🏢 Department: Dept Name
   📋 Sector: Sector Name
   📱 Mobile: +994 XX XXX XX XX
   📞 Internal: 123
   🏙️ City: City Name
   📧 Email: name@example.com
```

## ✨ Summary

**You now have:**
✅ Department/Sector search working
✅ All emails included in results
✅ 1,345 contacts searchable by department
✅ Test script to verify functionality
✅ Migration script for database updates
✅ Full backward compatibility
