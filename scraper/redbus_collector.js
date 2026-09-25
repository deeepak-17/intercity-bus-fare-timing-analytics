// BookSmart - redBus listing collector (run in the browser DevTools console on any https://www.redbus.in page)
//
// Why a browser script: script requests (curl/Python) could not reach the site from the analysis environment,
// so collection runs inside a normal browser session and calls the same JSON endpoint the search page uses. Only public listing data
// is read; no login, no booking, no personal data.
//
// Pass 1 pages through every listing for 8 corridors x 13 departure dates.
// Pass 2 expands the collapsed government-operator groups (APSRTC, TGSRTC, KSRTC, RSRTC, ...).
// At the end a CSV (bus_fares_raw_<date>.csv) is downloaded; put it in data/raw/.

(async () => {
  const SCRAPE_DATE = new Date(2026, 8, 25);            // 25 Sep 2026 (month is 0-based)
  const ROUTES = [                                       // [source, destination, fromCityId, toCityId]
    ['Bengaluru', 'Chennai', 122, 123], ['Bengaluru', 'Hyderabad', 122, 124],
    ['Chennai', 'Coimbatore', 123, 141], ['Bengaluru', 'Coimbatore', 122, 141],
    ['Hyderabad', 'Vijayawada', 124, 134], ['Mumbai', 'Pune', 462, 130],
    ['Chennai', 'Madurai', 123, 126], ['Delhi', 'Jaipur', 733, 807],
  ];
  const OFFSETS = [1, 2, 3, 4, 5, 6, 7, 10, 14, 21, 30, 45, 60];   // days ahead
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const fmt = (d) => String(d.getDate()).padStart(2, '0') + '-' + MONTHS[d.getMonth()] + '-' + d.getFullYear();
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const iso = SCRAPE_DATE.toISOString().slice(0, 10);

  const call = async (fc, tc, doj, groupId, offset, meta) => {
    const url = `/rpw/api/searchResults?fromCity=${fc}&toCity=${tc}&DOJ=${doj}&limit=100&offset=${offset}` +
      `&meta=${meta}&groupId=${groupId}&sectionId=0&sort=0&sortOrder=0&from=initialLoad&getUuid=true&bT=1&isFilterApplied=false`;
    const r = await fetch(url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
    return r.json();
  };

  const rows = [];
  const keep = (s, d, b) => {
    const fl = (b.fareList || []).filter((x) => x > 0);
    rows.push([iso, s, d, b.doj, b.travelsName, b.busType, b.isAc ? 1 : 0, b.isSleeper ? 1 : 0,
      (b.departureTime || '').slice(11, 16), (b.arrivalTime || '').slice(11, 16), b.journeyDurationMin,
      b.totalRatings, b.numberOfReviews, b.availableSeats, b.totalSeats,
      fl.length ? Math.min(...fl) : '', fl.length ? Math.max(...fl) : '', b.viaRt || '', b.serviceId]);
  };

  for (const [s, d, fc, tc] of ROUTES) {
    for (const o of OFFSETS) {
      const dt = new Date(SCRAPE_DATE); dt.setDate(dt.getDate() + o);
      const doj = fmt(dt);
      // pass 1: all listed buses, 100 per page (capped at 600 per route-date)
      let offset = 0, groups = [];
      while (true) {
        const j = await call(fc, tc, doj, 0, offset, true);
        if (offset === 0) groups = (j.data?.metaData?.sections || []).flatMap((x) => x.groups || []);
        const inv = j.data?.inventories || [];
        inv.forEach((b) => keep(s, d, b));
        offset += 100;
        if (inv.length < 100 || offset >= 600) break;
        await sleep(1200);
      }
      // pass 2: expand collapsed operator groups (government corporations)
      for (const g of groups) {
        let off = 0;
        while (true) {
          await sleep(1200);
          const k = await call(fc, tc, doj, g.operatorId, off, false);
          const inv = k.data?.inventories || [];
          inv.forEach((b) => keep(s, d, b));
          off += 100;
          if (inv.length < 100 || off >= 400) break;
        }
      }
      console.log(`${s}-${d} ${doj}: ${rows.length} rows so far`);
      await sleep(1500);                                  // polite delay between searches
    }
  }

  const H = ['scrape_date', 'source', 'destination', 'departure_date', 'operator', 'bus_type', 'is_ac', 'is_sleeper',
    'departure_time', 'arrival_time', 'duration_min', 'rating', 'num_reviews', 'seats_available', 'total_seats',
    'fare_min', 'fare_max', 'via', 'service_id'];
  const esc = (v) => { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
  const csv = [H.join(','), ...rows.map((r) => r.map(esc).join(','))].join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  a.download = `bus_fares_raw_${iso}.csv`;
  document.body.appendChild(a); a.click(); a.remove();
  console.log('done:', rows.length, 'rows');
})();
