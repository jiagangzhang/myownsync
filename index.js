'use strict';

const crypto = require('crypto');
const debug = require('debug');
const debug_debug = debug('debug');
const fs = require('fs');
const queryString = require('querystring');
const restify = require('restify');
const superagent = require('superagent');

const isBlank = function(valer) {
	if (valer === null || valer === undefined || valer === '')
		return true;
	else
		return false;
};

const addQuote = function(s) {
	return '"' + s + '"';
};

var createPreSignString = function(params, isSDK) {
	var sortedParams = {};
	var keys = Object.keys(params);

	if (!isSDK) {
		keys.sort();
	}
	// Object.keys(params).sort().forEach(function (key) {
	keys.forEach(function(key) {
		let val = params[key];

		if (['sign', 'sign_type'].indexOf(key) < 0 && !isBlank(val)) {
			sortedParams[key] = isSDK ? addQuote(val) : val;
		}
	});

	var preSignString = queryString.stringify(sortedParams, null, null, {
		encodeURIComponent: queryString.unescape
	});
	return preSignString;
};

const auth_login = function(req, res, next) {
	const domain = req.query.domain || 'test-mm.eastasia.cloudapp.azure.com';
	const server = `http://${domain}`;
	superagent
		.post(`${server}/api/auth/login`)
		.send({
			Username: 'henry1',
			Password: 'Mm@123456'
		})
		.end(function(err, res2) {
			if (err){
				//debug_debug(err);
				console.log(err);  //use console output to stream log file for supervisor
			}
			else {
				req.Token = res2.body.Token;
				req.UserKey = res2.body.UserKey;
			}
			return next();
		});
};

const order_create = function(req, res, next) {
	const domain = req.query.domain || 'test-mm.eastasia.cloudapp.azure.com';
	const server = `http://${domain}`;
	superagent
		.post(`${server}/api/order/create`)
		.set('Authorization', req.Token)
		.send({
			CultureCode: 'CHS',
			Skus: [{
				Qty: 1,
				SkuId: 150151
			}],
			UserAddressKey: '5f64a28a-57a4-4b3e-bf0c-b8338ec23495',
			UserKey: req.UserKey
		})
		.end(function(err, res2) {
			if (err){
				// debug_debug(err);
				console.log(err); //use console output to stream log file for supervisor
			}
			else {
				req.ParentOrderKey = res2.body.ParentOrderKey;
			}
			return next();
		});
};

const alipay_payment_create = function(req, res, next) {
	const domain = req.query.domain || 'test-mm.eastasia.cloudapp.azure.com';
	const server = `http://${domain}`;
	superagent
		.post(`${server}/api/alipay/payment/create`)
		.set('Authorization', req.Token)
		.send({
			body: 'Android Payment String',
			currency: 'HKD',
			forex_biz: 'FP',
			it_b_pay: '30m',
			out_trade_no: req.ParentOrderKey, // '17020641917697',
			payment_type: '1',
			product_code: 'NEW_WAP_OVERSEAS_SELLER',
			service: 'mobile.securitypay.pay',
			subject: 'MM Payment on Android',
			total_fee: 0.01
		})
		.end(function(err, res2) {
			if (err){
				// debug_debug(err);
				console.log(err);
			}
			else {
				req.alipay_payment_create_res = res2.body;
			}
			return next();
		});
};

const alipay_notify = function(req, res, next) {
	const out_trade_no = req.ParentOrderKey || req.query.ParentOrderKey;
	const now = new Date();
	const trade_no = req.query.trade_no || now.getTime();
	const notify_id = now.getTime();
	const batch_no = now.getTime();
	const gmt_create = now.toISOString();
	const notify_time = now.toISOString();
	const gmt_payment = now.toISOString();
	const total_fee = req.query.total_fee || 0.01;
	const price = req.query.price || 0.01;
	const return_amount = req.query.return_amount || 0.01;
	const quantity = req.query.quantity || 1;

	const notify_payment_payload = {
		discount: 0.00,
		payment_type: 1,
		subject: '美美',
		trade_no: trade_no, // '2017020621001004230251224677',
		buyer_email: 'wweco.test@gmail.com',
		gmt_create: gmt_create, // '2017-02-06 11:16:29',
		notify_type: 'trade_status_sync',
		quantity: quantity,
		out_trade_no: out_trade_no, // '17020641917697',
		seller_id: '2088121921332031',
		notify_time: notify_time, // '2017-02-06 11:16:30',
		body: '布克兄弟 (WWE): 蓝色男士修身西装 蓝色 XL *1',
		trade_status: 'TRADE_SUCCESS',
		is_total_fee_adjust: 'N',
		total_fee: total_fee,
		gmt_payment: gmt_payment, // '2017-02-06 11:16:30',
		seller_email: 'mmsh@waltonbrown.com.cn',
		price: price,
		buyer_id: '2088222759087235',
		notify_id: notify_id, // '87443ea5598e69464eaaf4b7e7f89f6hry',
		use_coupon: 'N',
		sign_type: 'RSA',
	};

	const domestic_refund_payload = {
		result_details: `${trade_no}^${return_amount}^SUCCESS`,//modified according to https://github.com/WWECO/mm-qa-tools/blob/master/api/controllers/alipay.js
		notify_time: notify_time,
		sign_type: 'RSA',
		notify_type: 'batch_refund_notify',
		notify_id: notify_id,
		batch_no: batch_no,
		success_num: 1
	};

	const global_refund_payload = {
		out_trade_no: out_trade_no,
		out_return_no: req.query.out_return_no,//modified according to https://github.com/WWECO/mm-qa-tools/blob/master/api/controllers/alipay.js
		return_amount: return_amount,
		notify_time: req.query.notify_time,
		sign_type: 'RSA',
		refund_status: 'REFUND_SUCCESS',
		notify_id: notify_id
	};


	let payload = notify_payment_payload;//modified according to https://github.com/WWECO/mm-qa-tools/blob/master/api/controllers/alipay.js
	if (req.query.notify_type === 'domestic_refund') {
		payload = domestic_refund_payload;
	} else if (req.query.notify_type === 'global_refund') {
		payload = global_refund_payload;
	} else if (req.query.notify_type === 'notify_payment_global') {
		payload = notify_payment_payload;
		payload.rmb_fee = payload.total_fee;
		delete payload.total_fee;
	}

	const plainText = createPreSignString(payload, false);

	const privateKey = fs.readFileSync('./mock_alipay_private_key.pem', 'utf8');

	const signer = crypto.createSign('RSA-SHA1', 'utf8');
	signer.update(plainText);
	payload.sign = signer.sign(privateKey, 'base64');

	// debug_debug(payload);
	console.log(payload); //use console output to stream log file for supervisor

	const domain = req.query.domain || 'test-mm.eastasia.cloudapp.azure.com';
	const server = `https://${domain}`;	// change to https if domain = load or other https only server
	superagent
		.post(`${server}/api/alipay/notify`)
		.send(payload)
		.end(function(err, res_from_mm) {
			if (err){
				// debug_debug(err);
				console.log(err);
				// res.status(406).send({
				// 	AppCode: err.toString(),
				// 	Details: err.toString(),
				// 	Message: err.toString()
				// });
				res.send(406, {Message: err.toString()});
			}
			else {
				// debug_debug(res_from_mm.text);
				console.log(res_from_mm.text);
				if (res_from_mm.text === 'fail'){
					// res.status(406).send({
					// 	AppCode: res_from_mm.text,
					// 	Details: res_from_mm.text,
					// 	Message: res_from_mm.text
					// });
					res.send(406, {Message: res_from_mm.text});
				} else {
					res.send(200, {
						alipay_payment_create_res: req.alipay_payment_create_res,
						ParentOrderKey: req.ParentOrderKey,
						trade_no: trade_no,
						notify_id: notify_id,
						batch_no: batch_no
					});
				}
			}
			return next();
		});
};

const gateway = function(req, res, next) {
	res.send(200, true);
	return next();
};

const server = restify.createServer();
server.use(restify.queryParser());
server.get('/alipay/mock/sample', auth_login, order_create, alipay_payment_create, alipay_notify);
server.get('/alipay/mock/notify', alipay_notify);
server.get('/alipay/mock/gateway.do', gateway);

server.listen(process.env.PORT || 8080, function() {
	// debug_debug('%s listening at %s', server.name, server.url);
	console.log('%s listening at %s', server.name, server.url);
});

// ===== DEMO SETUP =====
// in config.json
// ...
// "global":{
//   "refundAPI": "https://z9lz20fzktc9m8o4v0r8h9bypd4r5c.herokuapp.com/alipay/mock/gateway.do",
//   ...
//   "alipayPublicKey": "../pem/mock_alipay_public_key.pem"
// ...
// "china":{
//   "refundAPI": "https://z9lz20fzktc9m8o4v0r8h9bypd4r5c.herokuapp.com/alipay/mock/gateway.do",
//   ...
//   "alipayPublicKey": "../pem/mock_alipay_public_key.pem"
