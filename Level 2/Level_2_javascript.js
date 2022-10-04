var data = {
    "users": [
        {"id": 1, "name": "Nicolas", "objective": 1000},
        {"id": 2, "name": "Math", "objective": 500}
    ],
    "deals": [
        {"id": 1, "amount": 500, "user": 1},
        {"id": 2, "amount": 1000, "user": 2},
        {"id": 3, "amount": 800, "user": 1}
    ]
};

var users = data.users;
var deals = data.deals;

var commissions = [];

function calculateCommission(deal) {
    for (var i = 0; i < users.length; i++) {
        var user = users[i];
        var total = 0;
        var amount = 0;
        for (var j = 0; j < deals.length; j++) {
            var deal = deals[j];
            if (deal.user == user.id) {
                amount += deal.amount;
                if (amount <= user.objective * 0.5) {
                    total += deal.amount * 0.05;
                } 
                else if (amount <= user.objective && amount > user.objective * 0.5) {
                    if (amount - deal.amount < user.objective * 0.5) {
                        part_1 = deal.amount - (amount - user.objective * 0.5);
                        total += part_1 * 0.05 + (amount - user.objective * 0.5) * 0.1;
                    }
                    else {
                        total += deal.amount * 0.1;
                    }                
                } 
                else if (amount > user.objective) {
                    if (amount - deal.amount < user.objective * 0.5) {
                        part_1 = deal.amount - (amount - user.objective * 0.5);
                        part_2 = deal.amount - part_1 - (amount - user.objective);
                        total += part_1 * 0.05 + part_2 * 0.1 + (amount - user.objective) * 0.15;
                    }
                    else if (amount - deal.amount < user.objective) {
                        part_2 = deal.amount - (amount - user.objective);
                        total += part_2 * 0.1 + (amount - user.objective) * 0.15;
                    }
                    else {
                        total += deal.amount * 0.15;
                    }
                }
            }
        }
        commissions.push({
            "id": user.id,
            "name": user.name,
            "commission": total
        });
    }
}

calculateCommission(deals);
console.log(commissions);

